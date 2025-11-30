"""
Interactive Business Intelligence Dashboard - Final
Retail Analytics Platform
"""

import gradio as gr
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import tempfile

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from strategies.profiling_strategies import (
    BasicStatisticsStrategy, MissingValuesStrategy, NumericSummaryStrategy,
    CategoricalSummaryStrategy, DataQualityStrategy
)
from strategies.visualization_strategies import (
    TimeSeriesStrategy, DistributionStrategy, CategoryStrategy, CorrelationStrategy
)
from strategies.insight_strategies import (
    TopPerformersStrategy, AnomalyDetectionStrategy
)

class AppState:
    def __init__(self):
        self.original_data = None
        self.current_data = None

state = AppState()

# --- Data Processing ---
def load_data(file):
    if file is None:
        return "Please upload a file", None, None, None, None, None, gr.update(choices=[]), gr.update(choices=[])
    
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file.name)
        elif file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file.name)
        else:
            return "Invalid file type.", None, None, None, None, None, gr.update(choices=[]), gr.update(choices=[])
        
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_datetime(df[col])
                except:
                    pass

        state.original_data = df
        state.current_data = df
        
        preview = df.head(20)
        basic_stats = BasicStatisticsStrategy().process(df)
        stats_text = f"""
        **Rows:** {basic_stats['total_rows']:,} | **Cols:** {basic_stats['total_columns']}
        **Memory:** {basic_stats['memory_usage']}
        **Types:** {basic_stats['numeric_columns']} Numeric, {basic_stats['categorical_columns']} Categorical
        """
        
        missing_df = MissingValuesStrategy().process(df)
        if missing_df.empty: missing_df = pd.DataFrame({"Status": ["No missing values"]})
        
        numeric_df = NumericSummaryStrategy().process(df)
        quality = DataQualityStrategy().process(df)
        quality_text = f"**Completeness:** {quality['completeness']} | **Duplicates:** {quality['duplicate_rows']}"
        
        all_cols = df.columns.tolist()
        
        # Note: We return all_cols for Filter, but we will update Viz cols in the .then() event
        return (f"✅ Loaded {len(df)} rows", preview, stats_text, 
                missing_df, numeric_df, quality_text, 
                gr.update(choices=all_cols)) 
        
    except Exception as e:
        return f"❌ Error: {str(e)}", None, None, None, None, None, gr.update(choices=[])

def generate_categorical_summary():
    df = state.current_data
    if df is None: return "No data"
    strategy = CategoricalSummaryStrategy()
    summaries = strategy.process(df)
    output = ""
    for col, data in summaries.items():
        output += f"**{col}**\n{data.to_markdown()}\n\n"
    return output

def apply_filters(column, operation, value):
    df = state.original_data
    if df is None: return "No data loaded", None
    
    try:
        if not column or not value:
            return "Please select a column and enter a value", df.head()
            
        if operation == "Equals (==)":
            filtered = df[df[column].astype(str) == str(value)]
        elif operation == "Greater Than (>)":
            filtered = df[df[column] > float(value)]
        elif operation == "Less Than (<)":
            filtered = df[df[column] < float(value)]
        elif operation == "Contains":
            filtered = df[df[column].astype(str).str.contains(str(value), case=False, na=False)]
        else:
            filtered = df
            
        state.current_data = filtered
        return f"✅ Filtered: {len(filtered)} rows", filtered.head(20)
    except Exception as e:
        return f"❌ Filter Error: {str(e)}", df.head()

def reset_dataset():
    if state.original_data is not None:
        state.current_data = state.original_data
        return "🔄 Reset to original", state.current_data.head(20)
    return "No data", None

# --- Visualization & Insights ---
def update_viz_options(choice):
    """Dynamically update column dropdowns based on the selected chart type"""
    df = state.current_data
    if df is None: 
        return gr.update(choices=[]), gr.update(choices=[])
    
    all_cols = df.columns.tolist()
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    date_cols = df.select_dtypes(include=['datetime']).columns.tolist()
    
    # Logic to populate dropdowns with specific types
    if choice == "Time Series":
        return (gr.update(choices=date_cols, label="Date Column (X-Axis)", visible=True, value=None), 
                gr.update(choices=num_cols, label="Value Column (Y-Axis)", visible=True, value=None))
                
    elif choice == "Distribution":
        return (gr.update(choices=num_cols, label="Numeric Column", visible=True, value=None), 
                gr.update(visible=False))
                
    elif choice == "Bar Chart":
        return (gr.update(choices=cat_cols, label="Category Column", visible=True, value=None), 
                gr.update(choices=num_cols, label="Value Column (Y-Axis)", visible=True, value=None))
                
    elif choice == "Correlation":
        return (gr.update(visible=False), gr.update(visible=False))
    
    # Fallback
    return gr.update(choices=all_cols, visible=True), gr.update(choices=all_cols, visible=True)

def create_chart(chart_type, col1, col2):
    df = state.current_data
    if df is None: return None
    
    strategies = {
        "Time Series": TimeSeriesStrategy(),
        "Distribution": DistributionStrategy(),
        "Bar Chart": CategoryStrategy(),
        "Correlation": CorrelationStrategy()
    }
    
    strategy = strategies.get(chart_type)
    
    try:
        if chart_type == "Time Series":
            return strategy.create_visualization(df, date_column=col1, value_column=col2)
        elif chart_type == "Distribution":
            return strategy.create_visualization(df, column=col1)
        elif chart_type == "Bar Chart":
            return strategy.create_visualization(df, category_column=col1, value_column=col2, aggregation='sum')
        elif chart_type == "Correlation":
            return strategy.create_visualization(df)
    except Exception as e:
        print(f"Viz Error: {e}")
    return None

def generate_insights():
    df = state.current_data
    if df is None: return "No data loaded"
    perf = TopPerformersStrategy().process(df)
    anom = AnomalyDetectionStrategy().process(df)
    return f"{perf}\n\n---\n\n{anom}"

def export_current_data():
    df = state.current_data
    if df is None: return None
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
    df.to_csv(tmp.name, index=False)
    return tmp.name

# --- UI ---
with gr.Blocks(title="Retail BI Dashboard") as app:
    gr.Markdown("# 🛍️ Retail Business Intelligence Dashboard")
    
    with gr.Row():
        with gr.Column(scale=1):
            file_upload = gr.File(label="📁 1. Upload Dataset", file_types=[".csv", ".xlsx"])
            load_btn = gr.Button("🚀 Load Data", variant="primary")
            status_msg = gr.Textbox(label="System Status", interactive=False)
    
    with gr.Tabs():
        # Tab 1: Profile
        with gr.Tab("📊 Data Profile"):
            with gr.Row():
                basic_stats = gr.Markdown("### Basic Statistics")
                quality_stats = gr.Markdown("### Data Quality")
            
            with gr.Accordion("Detailed Categorical Analysis", open=False):
                cat_btn = gr.Button("Generate Categorical Summary")
                cat_output = gr.Markdown()
                cat_btn.click(generate_categorical_summary, None, cat_output)

            with gr.Row():
                missing_tbl = gr.Dataframe(label="Missing Values Analysis")
                numeric_tbl = gr.Dataframe(label="Numeric Summary")
            preview_tbl = gr.Dataframe(label="Data Preview (First 20 Rows)")

        # Tab 2: Filter
        with gr.Tab("🔍 Filter & Explore"):
            with gr.Row():
                filter_col = gr.Dropdown(label="Column")
                filter_op = gr.Dropdown(label="Operation", choices=["Equals (==)", "Greater Than (>)", "Less Than (<)", "Contains"])
                filter_val = gr.Textbox(label="Value")
            with gr.Row():
                apply_btn = gr.Button("Apply Filter")
                reset_btn = gr.Button("Reset Data")
            filtered_tbl = gr.Dataframe(label="Filtered Data Preview")
            export_btn = gr.Button("💾 Export Filtered CSV")
            download_file = gr.File(label="Download Export")

        # Tab 3: Visualizations
        with gr.Tab("📈 Visualizations"):
            with gr.Row():
                # Set a default value to ensure logic triggers correctly
                viz_type = gr.Dropdown(label="Chart Type", choices=["Time Series", "Distribution", "Bar Chart", "Correlation"], value="Time Series")
                viz_col1 = gr.Dropdown(label="Primary Column")
                viz_col2 = gr.Dropdown(label="Secondary Column")
            viz_gen_btn = gr.Button("Generate Chart", variant="primary")
            chart_output = gr.Plot()

        # Tab 4: Insights
        with gr.Tab("💡 Automated Insights"):
            insight_btn = gr.Button("Generate Smart Insights")
            insight_txt = gr.Markdown()

    # --- Event Wiring ---
    
    # 1. LOAD DATA: Update data state, profile tables, and filter dropdown
    load_btn.click(
        load_data, 
        inputs=[file_upload], 
        outputs=[status_msg, preview_tbl, basic_stats, missing_tbl, numeric_tbl, quality_stats, filter_col]
    ).then(
        # 2. THEN: Explicitly update Visualization columns based on the default "Time Series" selection
        fn=update_viz_options,
        inputs=[viz_type],
        outputs=[viz_col1, viz_col2]
    )
    
    # Filter Events
    apply_btn.click(apply_filters, [filter_col, filter_op, filter_val], [status_msg, filtered_tbl])
    reset_btn.click(reset_dataset, None, [status_msg, filtered_tbl])
    export_btn.click(export_current_data, None, download_file)
    
    # Viz Events
    viz_type.change(update_viz_options, viz_type, [viz_col1, viz_col2])
    viz_gen_btn.click(create_chart, [viz_type, viz_col1, viz_col2], chart_output)
    
    # Insight Events
    insight_btn.click(generate_insights, None, insight_txt)

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860)