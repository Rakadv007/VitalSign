"""
PCA Dimensionality Reduction Module
Computes Principal Component Analysis (PCA), explained variance ratios, cumulative variance curve,
and interactive 2D / 3D feature space scatterplots.
"""

import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from utils.config import RANDOM_STATE, PRIMARY_COLOR, SECONDARY_COLOR


def run_pca_reduction(df, target_col='readmitted', n_components=10, sample_size=5000):
    """
    Fits PCA on preprocessed numerical features and returns variance statistics and 2D/3D plots.
    """
    X = df.drop(columns=[target_col]) if target_col in df.columns else df.copy()
    X = X.select_dtypes(include=[np.number]).dropna()
    
    if len(X) > sample_size:
        X_sample = X.sample(n=sample_size, random_state=RANDOM_STATE)
        y_sample = df.loc[X_sample.index, target_col] if target_col in df.columns else None
    else:
        X_sample = X
        y_sample = df[target_col] if target_col in df.columns else None
        
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_sample)
    
    max_comps = min(n_components, X_scaled.shape[1])
    pca = PCA(n_components=max_comps, random_state=RANDOM_STATE)
    X_pca = pca.fit_transform(X_scaled)
    
    exp_var = pca.explained_variance_ratio_
    cum_var = np.cumsum(exp_var)
    
    variance_df = pd.DataFrame({
        'Component': [f"PC{i+1}" for i in range(max_comps)],
        'Explained Variance Ratio': np.round(exp_var, 4),
        'Cumulative Explained Variance': np.round(cum_var, 4)
    })
    
    # Scree Plot / Cumulative Variance Plot
    scree_fig = px.line(
        variance_df,
        x='Component',
        y='Cumulative Explained Variance',
        markers=True,
        title="PCA Cumulative Explained Variance Curve",
        color_discrete_sequence=[PRIMARY_COLOR]
    )
    scree_fig.add_bar(
        x=variance_df['Component'],
        y=variance_df['Explained Variance Ratio'],
        name="Individual Variance Ratio",
        marker_color=SECONDARY_COLOR
    )
    scree_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    
    # 2D Scatterplot
    pca_2d_df = pd.DataFrame({
        'PC1': X_pca[:, 0],
        'PC2': X_pca[:, 1],
        'Target': y_sample.values if y_sample is not None else 'Data'
    })
    
    fig_2d = px.scatter(
        pca_2d_df,
        x='PC1',
        y='PC2',
        color='Target' if y_sample is not None else None,
        title=f"2D PCA Projection (Explained Variance: {cum_var[1]*100:.1f}%)"
    )
    fig_2d.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    
    # 3D Scatterplot
    fig_3d = None
    if max_comps >= 3:
        pca_3d_df = pd.DataFrame({
            'PC1': X_pca[:, 0],
            'PC2': X_pca[:, 1],
            'PC3': X_pca[:, 2],
            'Target': y_sample.values if y_sample is not None else 'Data'
        })
        fig_3d = px.scatter_3d(
            pca_3d_df,
            x='PC1',
            y='PC2',
            z='PC3',
            color='Target' if y_sample is not None else None,
            title=f"3D PCA Projection (Explained Variance: {cum_var[2]*100:.1f}%)"
        )
        
    return {
        'variance_table': variance_df,
        'n_components': max_comps,
        'total_explained_variance': round(float(cum_var[-1]), 4),
        'scree_fig': scree_fig,
        'fig_2d': fig_2d,
        'fig_3d': fig_3d
    }
