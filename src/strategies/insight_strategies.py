"""
Concrete Insight Generation Strategies
"""
import pandas as pd
import numpy as np
from .base_strategy import DataProcessingStrategy

class TopPerformersStrategy(DataProcessingStrategy):
    def process(self, data: pd.DataFrame) -> str:
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        categorical_cols = data.select_dtypes(include=['object']).columns
        
        if len(numeric_cols) == 0 or len(categorical_cols) == 0:
            return "❌ Not enough data to generate top performers."
            
        insights = []
        target_num = numeric_cols[0] 
        target_cat = categorical_cols[0]
        
        top_perf = data.groupby(target_cat)[target_num].sum().sort_values(ascending=False).head(3)
        
        insights.append(f"### 🏆 Top 3 {target_cat} by {target_num}")
        for idx, value in top_perf.items():
            insights.append(f"- **{idx}**: {value:,.2f}")
            
        return "\n".join(insights)

    def get_description(self) -> str:
        return "Identifies top performers based on aggregation"

class AnomalyDetectionStrategy(DataProcessingStrategy):
    def process(self, data: pd.DataFrame) -> str:
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        insights = ["### ⚠️ Anomalies Detected"]
        
        has_anomalies = False
        for col in numeric_cols:
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = data[(data[col] < lower_bound) | (data[col] > upper_bound)]
            
            if not outliers.empty:
                has_anomalies = True
                insights.append(f"- **{col}**: {len(outliers)} outliers found (values outside {lower_bound:.2f} to {upper_bound:.2f})")
                
        if not has_anomalies:
            return "### ✅ No significant statistical anomalies detected."
            
        return "\n".join(insights)

    def get_description(self) -> str:
        return "Detects statistical outliers using IQR method"