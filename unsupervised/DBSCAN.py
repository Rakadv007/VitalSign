"""
DBSCAN Density-Based Clustering Module
Computes density clusters, distinguishes noise points (-1), and evaluates valid cluster silhouette scores.
"""

import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from utils.config import RANDOM_STATE


def run_dbscan(df, target_col='readmitted', eps=1.5, min_samples=10, sample_size=3000):
    """
    Runs DBSCAN density clustering on feature space.
    """
    X = df.drop(columns=[target_col]) if target_col in df.columns else df.copy()
    X = X.select_dtypes(include=[np.number]).dropna()
    
    if len(X) > sample_size:
        X_sample = X.sample(n=sample_size, random_state=RANDOM_STATE)
    else:
        X_sample = X
        
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_sample)
    
    db = DBSCAN(eps=eps, min_samples=min_samples)
    labels = db.fit_predict(X_scaled)
    
    total_samples = len(labels)
    noise_count = int((labels == -1).sum())
    noise_pct = round((noise_count / total_samples) * 100, 2)
    
    unique_clusters = set(labels) - {-1}
    num_clusters = len(unique_clusters)
    
    # Calculate Silhouette score on non-noise points if >1 cluster exists
    non_noise_mask = labels != -1
    sil_score = 0.0
    if num_clusters > 1 and non_noise_mask.sum() > num_clusters:
        try:
            sil_score = float(silhouette_score(X_scaled[non_noise_mask], labels[non_noise_mask]))
        except Exception:
            sil_score = 0.0
            
    # PCA 2D Plot
    pca = PCA(n_components=2, random_state=RANDOM_STATE)
    pca_2d = pca.fit_transform(X_scaled)
    
    cluster_str_labels = [f"Cluster {l}" if l != -1 else "Noise (-1)" for l in labels]
    
    pca_df = pd.DataFrame({
        'PCA1': pca_2d[:, 0],
        'PCA2': pca_2d[:, 1],
        'Cluster': cluster_str_labels
    })
    
    pca_fig = px.scatter(
        pca_df,
        x='PCA1',
        y='PCA2',
        color='Cluster',
        title=f"DBSCAN Clusters & Noise Projection (eps={eps}, min_samples={min_samples})",
        color_discrete_sequence=px.colors.qualitative.Dark24
    )
    pca_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    
    return {
        'eps': eps,
        'min_samples': min_samples,
        'num_clusters': num_clusters,
        'noise_count': noise_count,
        'noise_pct': noise_pct,
        'silhouette_score': round(sil_score, 4),
        'pca_fig': pca_fig
    }
