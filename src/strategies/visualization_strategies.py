"""
Concrete Visualization Strategies
Implements the Strategy Pattern for different visualization types using Plotly
"""
import pandas as pd
import plotly.express as px
from typing import Any, List
from .base_strategy import VisualizationStrategy

class TimeSeriesStrategy(VisualizationStrategy):
    def create_visualization(self, data: pd.DataFrame, **kwargs) -> Any:
        date_col = kwargs.get('date_column')
        value_col = kwargs.get('value_column')
        
        if not date_col or not value_col:
            return None
            
        # Ensure date sorting for correct line plotting
        daily_data = data.groupby(date_col)[value_col].sum().reset_index().sort_values(date_col)
        
        fig = px.line(daily_data, x=date_col, y=value_col, 
                      title=f'{value_col} Over Time',
                      template='plotly_white')
        return fig

    def get_name(self) -> str:
        return "Time Series Analysis"

    def get_required_columns(self) -> List[str]:
        return ['datetime', 'numeric']

class DistributionStrategy(VisualizationStrategy):
    def create_visualization(self, data: pd.DataFrame, **kwargs) -> Any:
        col = kwargs.get('column')
        if not col:
            return None
            
        fig = px.histogram(data, x=col, title=f'Distribution of {col}',
                          marginal="box",
                          template='plotly_white')
        return fig

    def get_name(self) -> str:
        return "Distribution Plot"

    def get_required_columns(self) -> List[str]:
        return ['numeric']

class CategoryStrategy(VisualizationStrategy):
    def create_visualization(self, data: pd.DataFrame, **kwargs) -> Any:
        cat_col = kwargs.get('category_column')
        val_col = kwargs.get('value_column')
        agg_func = kwargs.get('aggregation', 'count')
        
        if not cat_col:
            return None
            
        # Case 1: Count or no value column provided
        if agg_func == 'count' or not val_col:
            counts = data[cat_col].value_counts().reset_index()
            counts.columns = [cat_col, 'Count']
            return px.bar(counts, x=cat_col, y='Count', title=f'Count by {cat_col}',
                        template='plotly_white')
        
        # Case 2: Aggregation on value column
        if agg_func == 'mean':
            agg_data = data.groupby(cat_col)[val_col].mean().reset_index()
        else: 
            # Default to sum for 'sum' or any fallback
            agg_data = data.groupby(cat_col)[val_col].sum().reset_index()
            
        return px.bar(agg_data, x=cat_col, y=val_col, 
                    title=f'{agg_func.title()} of {val_col} by {cat_col}',
                    template='plotly_white')

    def get_name(self) -> str:
        return "Category Analysis"

    def get_required_columns(self) -> List[str]:
        return ['categorical']

class CorrelationStrategy(VisualizationStrategy):
    def create_visualization(self, data: pd.DataFrame, **kwargs) -> Any:
        numeric_df = data.select_dtypes(include=['number'])
        
        if len(numeric_df.columns) < 2:
            return None
            
        corr_matrix = numeric_df.corr()
        
        fig = px.imshow(corr_matrix, 
                       title='Correlation Heatmap',
                       text_auto=True,
                       template='plotly_white')
        return fig

    def get_name(self) -> str:
        return "Correlation Heatmap"

    def get_required_columns(self) -> List[str]:
        return ['numeric']