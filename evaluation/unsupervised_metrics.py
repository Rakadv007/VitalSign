"""
Unsupervised Learning Metrics Module
Calculates Silhouette Score, Calinski-Harabasz Index, and Davies-Bouldin Index when mathematically valid.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score


def compute_unsupervised_metrics(X, labels):
    """
    Computes clustering quality metrics. Excludes noise points (-1) if present.
    """
    labels = np.array(labels)
    valid_mask = labels != -1
    
    if valid_mask.sum() < 2:
        return {'status': 'Insufficient cluster points for evaluation'}
        
    X_valid = X[valid_mask]
    labels_valid = labels[valid_mask]
    
    unique_labels = np.unique(labels_valid)
    if len(unique_labels) < 2:
        return {'status': 'Fewer than 2 distinct clusters found'}
        
    sil = float(silhouette_score(X_valid, labels_valid))
    ch = float(calinski_harabasz_score(X_valid, labels_valid))
    db = float(davies_bouldin_score(X_valid, labels_valid))
    
    return {
        'Silhouette Score': round(sil, 4),
        'Calinski-Harabasz Index': round(ch, 2),
        'Davies-Bouldin Index': round(db, 4),
        'Evaluated Clusters': int(len(unique_labels)),
        'Valid Points': int(len(labels_valid))
    }
