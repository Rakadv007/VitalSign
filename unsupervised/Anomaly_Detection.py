"""
Anomaly Detection Module
Uses Isolation Forest algorithm to detect data outliers/anomalies in high-dimensional feature space.
Calculates exact anomaly counts, percentages, and 2D PCA visualizations.
"""

import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from utils.config import RANDOM_STATE, PRIMARY_COLOR


def run_anomaly_detection(df, target_col='readmitted', contamination=0.05, sample_size=5000):
    """
    Runs Isolation Forest to identify anomalous patient records.
    """
    X = df.drop(columns=[target_col]) if target_col in df.columns else df.copy()
    X = X.select_dtypes(include=[np.number]).dropna()
    
    if len(X) > sample_size:
        X_sample = X.sample(n=sample_size, random_state=RANDOM_STATE)
    else:
        X_sample = X
        
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_sample)
    
    iso = IsolationForest(contamination=contamination, random_state=RANDOM_STATE, n_jobs=-1)
    preds = iso.fit_predict(X_scaled)  # 1 = Normal, -1 = Anomaly
    
    anom_count = int((preds == -1).sum())
    norm_count = int((preds == 1).sum())
    anom_pct = round((anom_count / len(preds)) * 100, 2)
    
    # 2D PCA Visualization
    pca = PCA(n_components=2, random_state=RANDOM_STATE)
    pca_2d = pca.fit_transform(X_scaled)
    
    label_map = {1: 'Normal Record', -1: 'Anomaly Detected'}
    
    pca_df = pd.DataFrame({
        'PCA1': pca_2d[:, 0],
        'PCA2': pca_2d[:, 1],
        'Status': [label_map[p] for p in preds]
    })
    
    fig = px.scatter(
        pca_df,
        x='PCA1',
        y='PCA2',
        color='Status',
        color_discrete_map={'Normal Record': PRIMARY_COLOR, 'Anomaly Detected': '#EF4444'},
        title=f"Isolation Forest Anomaly Detection (Contamination = {contamination*100}%)"
    )
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    
    return {
        'contamination': contamination,
        'anomaly_count': anom_count,
        'normal_count': norm_count,
        'anomaly_pct': anom_pct,
        'pca_fig': fig
    }
