"""
Concrete Data Profiling Strategies
Implements the Strategy Pattern for different data profiling approaches
"""
import pandas as pd
import numpy as np
from typing import Dict, Any
from .base_strategy import DataProcessingStrategy


class BasicStatisticsStrategy(DataProcessingStrategy):
    """Strategy for computing basic statistical summaries"""
    
    def process(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Compute basic statistics for the dataset"""
        stats = {
            'total_rows': len(data),
            'total_columns': len(data.columns),
            'memory_usage': f"{data.memory_usage(deep=True).sum() / 1024**2:.2f} MB",
            'numeric_columns': len(data.select_dtypes(include=[np.number]).columns),
            'categorical_columns': len(data.select_dtypes(include=['object']).columns),
            'datetime_columns': len(data.select_dtypes(include=['datetime64']).columns),
        }
        return stats
    
    def get_description(self) -> str:
        return "Computes basic statistics like row count, column count, and data types"


class MissingValuesStrategy(DataProcessingStrategy):
    """Strategy for analyzing missing values"""
    
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        """Analyze missing values in the dataset"""
        missing_data = pd.DataFrame({
            'Column': data.columns,
            'Missing_Count': data.isnull().sum().values,
            'Missing_Percentage': (data.isnull().sum() / len(data) * 100).values,
            'Data_Type': data.dtypes.values
        })
        missing_data = missing_data[missing_data['Missing_Count'] > 0].sort_values(
            'Missing_Percentage', ascending=False
        ).reset_index(drop=True)
        return missing_data
    
    def get_description(self) -> str:
        return "Identifies and quantifies missing values in each column"


class NumericSummaryStrategy(DataProcessingStrategy):
    """Strategy for summarizing numeric columns"""
    
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate summary statistics for numeric columns"""
        numeric_data = data.select_dtypes(include=[np.number])
        if numeric_data.empty:
            return pd.DataFrame()
        
        summary = numeric_data.describe().T
        summary['median'] = numeric_data.median()
        summary['mode'] = numeric_data.mode().iloc[0] if not numeric_data.mode().empty else np.nan
        summary['skewness'] = numeric_data.skew()
        summary['kurtosis'] = numeric_data.kurtosis()
        
        # Reorder columns
        cols = ['count', 'mean', 'median', 'mode', 'std', 'min', '25%', '50%', '75%', 'max', 'skewness', 'kurtosis']
        return summary[[col for col in cols if col in summary.columns]]
    
    def get_description(self) -> str:
        return "Provides detailed statistical summary of numeric columns"


class CategoricalSummaryStrategy(DataProcessingStrategy):
    """Strategy for summarizing categorical columns"""
    
    def process(self, data: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Generate summary for categorical columns"""
        categorical_data = data.select_dtypes(include=['object'])
        if categorical_data.empty:
            return {}
        
        summaries = {}
        for col in categorical_data.columns:
            value_counts = data[col].value_counts()
            summary = pd.DataFrame({
                'Value': value_counts.index,
                'Count': value_counts.values,
                'Percentage': (value_counts.values / len(data) * 100).round(2)
            }).head(10)  # Top 10 categories
            summaries[col] = summary
        
        return summaries
    
    def get_description(self) -> str:
        return "Summarizes categorical columns with value counts and percentages"


class DataQualityStrategy(DataProcessingStrategy):
    """Strategy for assessing overall data quality"""
    
    def process(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Assess data quality metrics"""
        quality_report = {
            'completeness': f"{((1 - data.isnull().sum().sum() / (len(data) * len(data.columns))) * 100):.2f}%",
            'duplicate_rows': data.duplicated().sum(),
            'duplicate_percentage': f"{(data.duplicated().sum() / len(data) * 100):.2f}%",
        }
        
        # Check for potential issues in numeric columns
        numeric_data = data.select_dtypes(include=[np.number])
        if not numeric_data.empty:
            quality_report['columns_with_zeros'] = (numeric_data == 0).any().sum()
            quality_report['columns_with_negatives'] = (numeric_data < 0).any().sum()
            quality_report['columns_with_outliers'] = self._count_outlier_columns(numeric_data)
        
        return quality_report
    
    def _count_outlier_columns(self, numeric_data: pd.DataFrame) -> int:
        """Count columns that contain outliers using IQR method"""
        outlier_columns = 0
        for col in numeric_data.columns:
            Q1 = numeric_data[col].quantile(0.25)
            Q3 = numeric_data[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((numeric_data[col] < (Q1 - 1.5 * IQR)) | 
                       (numeric_data[col] > (Q3 + 1.5 * IQR))).any()
            if outliers:
                outlier_columns += 1
        return outlier_columns
    
    def get_description(self) -> str:
        return "Evaluates overall data quality including completeness and duplicates"
