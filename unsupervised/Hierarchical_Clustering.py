"""
Hierarchical Clustering Module
Performs Agglomerative Clustering, generates dendrogram tree plots, and evaluates silhouette scores.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from utils.config import RANDOM_STATE, PRIMARY_COLOR


def run_hierarchical_clustering(df, target_col='readmitted', n_clusters=3, sample_size=2000):
    """
    Computes linkage matrix, dendrogram plot, and Agglomerative Clustering results.
    """
    X = df.drop(columns=[target_col]) if target_col in df.columns else df.copy()
    X = X.select_dtypes(include=[np.number]).dropna()
    
    if len(X) > sample_size:
        X_sample = X.sample(n=sample_size, random_state=RANDOM_STATE)
    else:
        X_sample = X
        
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_sample)
    
    # Compute Linkage
    Z = linkage(X_scaled, method='ward')
    
    # Render Dendrogram
    fig, ax = plt.subplots(figsize=(10, 5))
    dendrogram(Z, p=30, truncate_mode='lastp', ax=ax, color_threshold=Z[-n_clusters+1, 2] if n_clusters > 1 else None)
    ax.set_title(f"Hierarchical Clustering Dendrogram (Truncated Top 30 Branches)")
    ax.set_xlabel("Sample Index / Cluster Size")
    ax.set_ylabel("Distance")
    plt.tight_layout()
    
    # Fit Agglomerative Model
    agg = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
    labels = agg.fit_predict(X_scaled)
    
    sil = float(silhouette_score(X_scaled, labels)) if len(np.unique(labels)) > 1 else 0.0
    cluster_counts = pd.Series(labels).value_counts().sort_index().to_dict()
    
    return {
        'n_clusters': n_clusters,
        'silhouette_score': round(sil, 4),
        'cluster_counts': {f"Cluster {k}": v for k, v in cluster_counts.items()},
        'dendrogram_fig': fig
    }
