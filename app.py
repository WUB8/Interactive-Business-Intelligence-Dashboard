"""
Interactive Business Intelligence Dashboard - Week 1 Foundation
Retail Domain Focus

Features:
- Data upload and preview
- Data profiling (statistics, missing values, quality assessment)
- Strategy Pattern implementation
"""

import gradio as gr
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from strategies.profiling_strategies import (
    BasicStatisticsStrategy,
    MissingValuesStrategy,
    NumericSummaryStrategy,
    CategoricalSummaryStrategy,
    DataQualityStrategy
)

# Global variable to store uploaded data
current_data = None


def load_data(file):
    """Load data from uploaded file"""
    global current_data
    
    if file is None:
        return "Please upload a file", None, None, None, None, None
    
    try:
        # Determine file type and load accordingly
        if file.name.endswith('.csv'):
            df = pd.read_csv(file.name)
        elif file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file.name)
        else:
            return "Unsupported file format. Please upload CSV or Excel file.", None, None, None, None, None
        
        current_data = df
        
        # Generate all profiling information
        preview = df.head(20)
        basic_stats = get_basic_statistics()
        missing_vals = get_missing_values_analysis()
        numeric_summary = get_numeric_summary()
        quality_report = get_data_quality()
        
        success_msg = f"✅ Data loaded successfully! {len(df)} rows and {len(df.columns)} columns."
        
        return success_msg, preview, basic_stats, missing_vals, numeric_summary, quality_report
        
    except Exception as e:
        return f"❌ Error loading file: {str(e)}", None, None, None, None, None


def get_basic_statistics():
    """Get basic statistics using Strategy Pattern"""
    global current_data
    
    if current_data is None:
        return "No data loaded"
    
    strategy = BasicStatisticsStrategy()
    stats = strategy.process(current_data)
    
    # Format as readable text
    output = f"""
📊 **Dataset Overview**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Total Rows: {stats['total_rows']:,}
📋 Total Columns: {stats['total_columns']}
💾 Memory Usage: {stats['memory_usage']}

**Column Types:**
🔢 Numeric Columns: {stats['numeric_columns']}
📝 Categorical Columns: {stats['categorical_columns']}
📅 DateTime Columns: {stats['datetime_columns']}

**Strategy Used:** {strategy.get_description()}
    """
    return output


def get_missing_values_analysis():
    """Analyze missing values using Strategy Pattern"""
    global current_data
    
    if current_data is None:
        return None
    
    strategy = MissingValuesStrategy()
    missing_df = strategy.process(current_data)
    
    if missing_df.empty:
        return pd.DataFrame({'Message': ['✅ No missing values found in the dataset!']})
    
    return missing_df


def get_numeric_summary():
    """Get numeric column summary using Strategy Pattern"""
    global current_data
    
    if current_data is None:
        return None
    
    strategy = NumericSummaryStrategy()
    summary = strategy.process(current_data)
    
    if summary.empty:
        return pd.DataFrame({'Message': ['No numeric columns found in the dataset']})
    
    return summary.round(2)


def get_categorical_summary():
    """Get categorical column summary using Strategy Pattern"""
    global current_data
    
    if current_data is None:
        return "No data loaded"
    
    strategy = CategoricalSummaryStrategy()
    summaries = strategy.process(current_data)
    
    if not summaries:
        return "No categorical columns found in the dataset"
    
    output = "📊 **Categorical Columns Summary**\n\n"
    for col, summary_df in summaries.items():
        output += f"**{col}** (Unique values: {len(current_data[col].unique())})\n"
        output += summary_df.to_markdown(index=False)
        output += "\n\n"
    
    return output


def get_data_quality():
    """Get data quality report using Strategy Pattern"""
    global current_data
    
    if current_data is None:
        return "No data loaded"
    
    strategy = DataQualityStrategy()
    quality = strategy.process(current_data)
    
    output = f"""
🎯 **Data Quality Report**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ Completeness: {quality['completeness']}
🔄 Duplicate Rows: {quality['duplicate_rows']} ({quality['duplicate_percentage']})
"""
    
    if 'columns_with_zeros' in quality:
        output += f"0️⃣ Columns with Zeros: {quality['columns_with_zeros']}\n"
        output += f"➖ Columns with Negatives: {quality['columns_with_negatives']}\n"
        output += f"📈 Columns with Outliers: {quality['columns_with_outliers']}\n"
    
    output += f"\n**Strategy Used:** {strategy.get_description()}"
    
    return output


def get_column_info():
    """Get detailed information about each column"""
    global current_data
    
    if current_data is None:
        return None
    
    info_data = []
    for col in current_data.columns:
        info_data.append({
            'Column': col,
            'Type': str(current_data[col].dtype),
            'Non-Null Count': current_data[col].count(),
            'Null Count': current_data[col].isnull().sum(),
            'Unique Values': current_data[col].nunique(),
            'Sample Values': str(current_data[col].dropna().head(3).tolist()[:3])
        })
    
    return pd.DataFrame(info_data)


# Create Gradio Interface
with gr.Blocks(title="Retail BI Dashboard - Week 1", theme=gr.themes.Soft()) as app:
    
    gr.Markdown("""
    # 🛍️ Interactive Business Intelligence Dashboard
    ## Retail Analytics Platform - Week 1 Foundation
    
    **Domain:** E-commerce / Retail  
    **Focus:** Data Upload, Preview, and Profiling
    
    Upload your retail dataset (CSV or Excel) to begin analysis.
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(label="📁 Upload Dataset (CSV or Excel)", file_types=['.csv', '.xlsx', '.xls'])
            load_button = gr.Button("🚀 Load and Analyze Data", variant="primary", size="lg")
            status_output = gr.Textbox(label="Status", lines=2)
            
            gr.Markdown("""
            ### 📊 Sample Dataset Available
            A sample retail dataset is included in the `data/` folder:
            - **online_retail.csv**: 5000 transactions across multiple categories
            """)
    
    with gr.Tabs():
        with gr.Tab("📋 Data Preview"):
            preview_output = gr.Dataframe(label="First 20 Rows", wrap=True)
        
        with gr.Tab("📊 Basic Statistics"):
            basic_stats_output = gr.Markdown()
        
        with gr.Tab("❓ Missing Values"):
            missing_vals_output = gr.Dataframe(label="Missing Values Analysis")
        
        with gr.Tab("🔢 Numeric Summary"):
            numeric_summary_output = gr.Dataframe(label="Numeric Columns Statistics")
        
        with gr.Tab("🏷️ Categorical Summary"):
            categorical_summary_output = gr.Markdown()
        
        with gr.Tab("✅ Data Quality"):
            quality_output = gr.Markdown()
        
        with gr.Tab("📝 Column Details"):
            column_info_output = gr.Dataframe(label="Column Information")
    
    # Event handlers
    load_button.click(
        fn=load_data,
        inputs=[file_input],
        outputs=[
            status_output,
            preview_output,
            basic_stats_output,
            missing_vals_output,
            numeric_summary_output,
            quality_output
        ]
    )
    
    # Add categorical summary button
    with gr.Row():
        categorical_button = gr.Button("📊 Generate Categorical Summary")
        column_info_button = gr.Button("📋 Show Column Details")
    
    categorical_button.click(
        fn=get_categorical_summary,
        outputs=categorical_summary_output
    )
    
    column_info_button.click(
        fn=get_column_info,
        outputs=column_info_output
    )
    
    gr.Markdown("""
    ---
    ### 🎯 Week 1 Completed Features:
    - ✅ Project structure set up
    - ✅ Retail domain selected with sample dataset
    - ✅ Data upload and preview functionality
    - ✅ Data profiling with multiple strategies:
      - Basic Statistics Strategy
      - Missing Values Analysis Strategy
      - Numeric Summary Strategy
      - Categorical Summary Strategy
      - Data Quality Assessment Strategy
    
    ### 🏗️ Architecture:
    This dashboard implements the **Strategy Pattern** for data processing:
    - **Base Strategy**: Abstract interface defining the contract
    - **Concrete Strategies**: Multiple implementations for different profiling approaches
    - **Benefits**: Easy to extend, maintain, and test different profiling methods
    
    ### 📚 Next Steps (Week 2):
    - Complete data profiling features
    - Create filtering interface
    - Begin visualization implementations
    """)


if __name__ == "__main__":
    app.launch(share=False, server_name="0.0.0.0", server_port=7860)
