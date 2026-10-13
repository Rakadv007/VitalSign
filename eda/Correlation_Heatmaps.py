"""
Target & Multi-feature Correlation Analysis Module
Ranks numerical feature correlations with target and extracts top collinear feature pairs.
"""

import pandas as pd
import numpy as np


def get_top_correlations(df, target_col='readmitted', top_n=10):
    """
    Calculates feature-to-target correlations (if target is numerical) or top pairwise collinearities.
    """
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(num_cols) < 2:
        return pd.DataFrame()
        
    corr_matrix = df[num_cols].corr().abs()
    
    # Extract upper triangle of correlation matrix
    upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    
    pairs = []
    for col1 in upper_tri.columns:
        for col2 in upper_tri.index:
            val = upper_tri.loc[col2, col1]
            if not np.isnan(val):
                pairs.append({
                    'Feature 1': col2,
                    'Feature 2': col1,
                    'Absolute Correlation': round(float(val), 3)
                })
                
    pairs_df = pd.DataFrame(pairs).sort_values(by='Absolute Correlation', ascending=False).head(top_n)
    return pairs_df.reset_index(drop=True)
