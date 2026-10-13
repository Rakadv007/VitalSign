"""
K-Means Clustering Module
Calculates inertia across multiple values of K to produce actual Elbow Curve.
Evaluates Silhouette Scores, cluster sizes, and 2D/3D PCA cluster projections.
"""

import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from utils.config import RANDOM_STATE, PRIMARY_COLOR


def run_kmeans_clustering(df, target_col='readmitted', k_range=range(2, 9), sample_size=5000):
    """
    Runs K-Means across K values on preprocessed numerical feature space (excluding target).
    """
    X = df.drop(columns=[target_col]) if target_col in df.columns else df.copy()
    X = X.select_dtypes(include=[np.number]).dropna()
    
    # Subsample if dataset is large for computational efficiency of silhouette calculation
    if len(X) > sample_size:
        X_sample = X.sample(n=sample_size, random_state=RANDOM_STATE)
    else:
        X_sample = X
        
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_sample)
    
    inertias = []
    silhouette_scores = []
    
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
        labels = km.fit_predict(X_scaled)
        inertias.append(float(km.inertia_))
        
        sil = float(silhouette_score(X_scaled, labels))
        silhouette_scores.append(round(sil, 4))
        
    elbow_df = pd.DataFrame({
        'K': list(k_range),
        'Inertia': inertias,
        'Silhouette Score': silhouette_scores
    })
    
    # Optimal K with highest silhouette score
    best_k = elbow_df.loc[elbow_df['Silhouette Score'].idxmax()]['K']
    best_km = KMeans(n_clusters=int(best_k), random_state=RANDOM_STATE, n_init=10)
    best_labels = best_km.fit_predict(X_scaled)
    
    # PCA 2D Visualization
    pca = PCA(n_components=2, random_state=RANDOM_STATE)
    pca_2d = pca.fit_transform(X_scaled)
    
    pca_df = pd.DataFrame({
        'PCA1': pca_2d[:, 0],
        'PCA2': pca_2d[:, 1],
        'Cluster': [f"Cluster {l}" for l in best_labels]
    })
    
    pca_fig = px.scatter(
        pca_df,
        x='PCA1',
        y='PCA2',
        color='Cluster',
        title=f"K-Means PCA 2D Cluster Visualization (K={int(best_k)})",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    pca_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    
    cluster_counts = pd.Series(best_labels).value_counts().sort_index().to_dict()
    
    return {
        'elbow_table': elbow_df,
        'best_k': int(best_k),
        'best_inertia': round(float(best_km.inertia_), 2),
        'best_silhouette': round(float(elbow_df['Silhouette Score'].max()), 4),
        'cluster_counts': {f"Cluster {k}": v for k, v in cluster_counts.items()},
        'pca_fig': pca_fig
    }
