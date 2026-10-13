"""
Target Variable Distribution & Imbalance Module
Provides distribution analysis for classification (counts, percentages, imbalance metrics)
and continuous target metrics for regression tasks.
"""

import pandas as pd
import numpy as np
from utils.plotting import create_target_distribution_chart


def analyze_target_distribution(df, target_col='readmitted'):
    """
    Computes exact target distribution metrics and checks class imbalance.
    """
    if target_col not in df.columns:
        return {'status': 'Target column not found', 'df': pd.DataFrame()}
        
    series = df[target_col].dropna()
    total = len(series)
    is_numeric = pd.api.types.is_numeric_dtype(series)
    is_continuous = is_numeric and (series.nunique() > 5 or target_col == 'time_in_hospital')
    
    if is_continuous:
        # Continuous numerical target statistics
        stats = {
            'mean': round(float(series.mean()), 3),
            'std': round(float(series.std()), 3),
            'median': round(float(series.median()), 3),
            'min': round(float(series.min()), 3),
            'max': round(float(series.max()), 3),
            'q25': round(float(series.quantile(0.25)), 3),
            'q75': round(float(series.quantile(0.75)), 3)
        }
        return {
            'task_type': 'regression',
            'stats': stats,
            'series': series
        }
    else:
        # Classification target distribution
        val_counts = series.value_counts()
        pcts = (val_counts / total * 100).round(2)
        
        dist_df = pd.DataFrame({
            'Target Value': val_counts.index.astype(str),
            'Count': val_counts.values,
            'Percentage (%)': pcts.values
        })
        
        # Imbalance ratio: majority class count / minority class count
        imbalance_ratio = round(val_counts.max() / val_counts.min(), 2) if len(val_counts) > 1 else 1.0
        
        chart = create_target_distribution_chart(dist_df, title=f"Target Distribution for '{target_col}'")
        
        return {
            'task_type': 'classification',
            'num_classes': len(val_counts),
            'distribution_table': dist_df,
            'imbalance_ratio': imbalance_ratio,
            'is_imbalanced': imbalance_ratio > 1.5,
            'chart': chart
        }
