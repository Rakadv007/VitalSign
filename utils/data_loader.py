"""
Vital Sign Data Loader Utility
Provides standardized methods for loading datasets, replacing missing value placeholders,
inspecting structure, and extracting dataset metadata safely.
"""

import os
import pandas as pd
import numpy as np
from utils.config import DATASET_CSV, PREPROCESSED_CSV, MISSING_VALUES_REPRESENTATION, ID_COLUMNS, DEFAULT_TARGET_COL


def load_raw_data(filepath=None):
    """
    Load raw dataset from diabetic_data.csv (or specified path), converting missing value
    indicators like '?' into numpy NaN.
    """
    path = filepath if filepath else DATASET_CSV
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found at {path}")
    
    # Load dataset
    df = pd.read_csv(path, low_memory=False)
    
    # Standardize missing values ('?' -> NaN)
    df = df.replace(MISSING_VALUES_REPRESENTATION, np.nan)
    return df


def load_processed_data(filepath=None):
    """
    Load processed dataset from preprocessed_dataset.csv.
    """
    path = filepath if filepath else PREPROCESSED_CSV
    if not os.path.exists(path):
        # Fallback to load raw data if processed file not yet generated
        return load_raw_data()
    df = pd.read_csv(path, low_memory=False)
    return df


def get_dataset_overview(df, target_col=DEFAULT_TARGET_COL):
    """
    Returns dynamically computed dataset statistics.
    """
    total_rows, total_cols = df.shape
    
    # Identify non-target, non-ID columns
    feature_cols = [c for c in df.columns if c != target_col and c not in ID_COLUMNS]
    
    # Numerical vs Categorical features
    num_cols = df[feature_cols].select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df[feature_cols].select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Target info
    target_info = {}
    if target_col in df.columns:
        target_series = df[target_col].dropna()
        target_type = str(target_series.dtype)
        unique_vals = target_series.nunique()
        value_counts = target_series.value_counts()
        percentage = (value_counts / len(target_series) * 100).round(2)
        
        target_dist_df = pd.DataFrame({
            'Target Value': value_counts.index.astype(str),
            'Count': value_counts.values,
            'Percentage (%)': percentage.values
        })
        
        target_info = {
            'name': target_col,
            'data_type': target_type,
            'unique_count': unique_vals,
            'distribution_table': target_dist_df,
            'is_continuous': pd.api.types.is_numeric_dtype(target_series) and unique_vals > 20
        }
    else:
        target_info = {
            'name': 'Not Found',
            'data_type': 'N/A',
            'unique_count': 0,
            'distribution_table': pd.DataFrame(),
            'is_continuous': False
        }
        
    summary = {
        'dataset_name': os.path.basename(DATASET_CSV),
        'total_rows': total_rows,
        'total_cols': total_cols,
        'num_features_count': len(num_cols),
        'cat_features_count': len(cat_cols),
        'num_cols': num_cols,
        'cat_cols': cat_cols,
        'feature_cols': feature_cols,
        'target_info': target_info,
        'memory_mb': round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
        'duplicate_rows': df.duplicated().sum(),
        'missing_cells_total': int(df.isnull().sum().sum())
    }
    return summary
