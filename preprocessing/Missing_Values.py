"""
Missing Values Analysis & Imputation Module
Inspects dataset missingness, generates report, and applies mathematically sound imputation methods.
"""

import pandas as pd
import numpy as np


def analyze_missing_values(df):
    """
    Computes exact missing value counts, percentages, and total missing cells.
    """
    total_cells = df.size
    total_missing = int(df.isnull().sum().sum())
    missing_pct_total = round((total_missing / total_cells) * 100, 2)
    
    missing_series = df.isnull().sum()
    cols_with_missing = missing_series[missing_series > 0]
    
    report_df = pd.DataFrame({
        'Column': cols_with_missing.index,
        'Missing Count': cols_with_missing.values,
        'Missing Percentage (%)': (cols_with_missing.values / len(df) * 100).round(2),
        'Data Type': [str(df[col].dtype) for col in cols_with_missing.index]
    }).sort_values(by='Missing Count', ascending=False).reset_index(drop=True)
    
    return {
        'total_missing_cells': total_missing,
        'missing_percentage_total': missing_pct_total,
        'cols_with_missing_count': len(cols_with_missing),
        'report_table': report_df
    }


def handle_missing_values(df, drop_threshold=0.70):
    """
    Treats missing values:
    - Drops columns missing > drop_threshold (e.g. >70% missingness).
    - Imputes numerical missing values with Median.
    - Imputes categorical missing values with Mode or 'Unknown'.
    Returns treated dataframe and a treatment log list.
    """
    df_treated = df.copy()
    treatment_log = []
    
    missing_pcts = df_treated.isnull().mean()
    cols_to_drop = missing_pcts[missing_pcts > drop_threshold].index.tolist()
    
    if cols_to_drop:
        df_treated = df_treated.drop(columns=cols_to_drop)
        for col in cols_to_drop:
            pct = round(missing_pcts[col] * 100, 2)
            treatment_log.append({
                'column': col,
                'action': 'Dropped column',
                'reason': f'Missing percentage ({pct}%) exceeded threshold of {drop_threshold*100}%'
            })
            
    # Impute remaining missing values
    for col in df_treated.columns:
        null_count = df_treated[col].isnull().sum()
        if null_count > 0:
            if pd.api.types.is_numeric_dtype(df_treated[col]):
                median_val = df_treated[col].median()
                df_treated[col] = df_treated[col].fillna(median_val)
                treatment_log.append({
                    'column': col,
                    'action': 'Median Imputation',
                    'reason': f'Imputed {null_count} missing numerical entries with median value ({median_val})'
                })
            else:
                # Categorical column - use mode or 'Unknown'
                mode_val = df_treated[col].mode()[0] if not df_treated[col].mode().empty else 'Unknown'
                df_treated[col] = df_treated[col].fillna(mode_val)
                treatment_log.append({
                    'column': col,
                    'action': 'Mode/Categorical Imputation',
                    'reason': f'Imputed {null_count} missing categorical entries with mode value ("{mode_val}")'
                })
                
    return df_treated, treatment_log
