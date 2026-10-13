"""
Outlier Detection & Treatment Module
Uses IQR (Interquartile Range) method to detect outliers in numerical features.
Calculates bounds, outlier counts, and percentages, and provides capping/winsorization logic.
"""

import pandas as pd
import numpy as np


def detect_outliers_iqr(df, num_cols=None):
    """
    Computes IQR, lower bound, upper bound, outlier count, and percentage per numerical feature.
    """
    if num_cols is None:
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
    outlier_summary = []
    
    for col in num_cols:
        series = df[col].dropna()
        if len(series) == 0:
            continue
            
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers_mask = (series < lower_bound) | (series > upper_bound)
        outlier_count = int(outliers_mask.sum())
        outlier_pct = round((outlier_count / len(series)) * 100, 2)
        
        outlier_summary.append({
            'Feature': col,
            'Q1 (25%)': round(float(Q1), 3),
            'Q3 (75%)': round(float(Q3), 3),
            'IQR': round(float(IQR), 3),
            'Lower Bound': round(float(lower_bound), 3),
            'Upper Bound': round(float(upper_bound), 3),
            'Outlier Count': outlier_count,
            'Outlier Pct (%)': outlier_pct
        })
        
    return pd.DataFrame(outlier_summary)


def handle_outliers_winsorize(df, num_cols=None, lower_quantile=0.01, upper_quantile=0.99):
    """
    Caps numerical features at specified percentile bounds (Winsorization) to reduce extreme variance
    without removing data records.
    Returns treated dataframe and treatment log.
    """
    df_treated = df.copy()
    if num_cols is None:
        num_cols = df_treated.select_dtypes(include=[np.number]).columns.tolist()
        
    treatment_log = []
    
    for col in num_cols:
        series = df_treated[col].dropna()
        if len(series) == 0:
            continue
            
        lower_limit = series.quantile(lower_quantile)
        upper_limit = series.quantile(upper_quantile)
        
        clipped = np.clip(df_treated[col], lower_limit, upper_limit)
        num_clipped = int((df_treated[col] != clipped).sum())
        
        df_treated[col] = clipped
        
        treatment_log.append({
            'feature': col,
            'action': 'Winsorization / Capping',
            'clipped_count': num_clipped,
            'lower_limit': round(float(lower_limit), 3),
            'upper_limit': round(float(upper_limit), 3)
        })
        
    return df_treated, treatment_log
