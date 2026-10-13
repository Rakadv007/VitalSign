"""
Numerical Correlation Heatmap Module
Computes Pearson correlation matrix across numerical features and produces interactive heatmaps.
"""

import pandas as pd
import numpy as np
from utils.plotting import create_correlation_heatmap_fig


def compute_correlation_matrix(df, num_cols=None, method='pearson'):
    """
    Computes pairwise correlation matrix for numerical features.
    """
    if num_cols is None:
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
    if len(num_cols) < 2:
        return pd.DataFrame()
        
    corr_df = df[num_cols].corr(method=method).round(3)
    return corr_df


def generate_heatmap_figure(df, num_cols=None, method='pearson'):
    """
    Returns Plotly figure object for correlation heatmap.
    """
    corr_df = compute_correlation_matrix(df, num_cols=num_cols, method=method)
    if corr_df.empty:
        return None
    return create_correlation_heatmap_fig(corr_df, title=f"Pearson Correlation Matrix ({len(num_cols)} Numerical Features)")
