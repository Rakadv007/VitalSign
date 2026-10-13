"""
Supervised Learning Metrics Module
Provides standardized evaluation routines for both Classification and Regression tasks.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix,
    mean_absolute_error, mean_squared_error, r2_score
)


def compute_classification_metrics(y_true, y_pred, y_proba=None, average='macro'):
    """
    Computes Accuracy, Precision, Recall, F1-score, and ROC-AUC.
    """
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average=average, zero_division=0)
    rec = recall_score(y_true, y_pred, average=average, zero_division=0)
    f1 = f1_score(y_true, y_pred, average=average, zero_division=0)
    
    roc_auc = 0.0
    if y_proba is not None:
        try:
            if len(np.unique(y_true)) == 2:
                roc_auc = roc_auc_score(y_true, y_proba[:, 1])
            else:
                roc_auc = roc_auc_score(y_true, y_proba, multi_class='ovr', average=average)
        except Exception:
            roc_auc = 0.0
            
    cm = confusion_matrix(y_true, y_pred)
    
    return {
        'Accuracy': round(float(acc), 4),
        'Precision': round(float(prec), 4),
        'Recall': round(float(rec), 4),
        'F1-Score': round(float(f1), 4),
        'ROC-AUC': round(float(roc_auc), 4),
        'Confusion Matrix': cm
    }


def compute_regression_metrics(y_true, y_pred, p=1):
    """
    Computes MAE, MSE, RMSE, R2, and Adjusted R2.
    """
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    
    n = len(y_true)
    adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1) if (n - p - 1) > 0 else r2
    
    return {
        'MAE': round(float(mae), 4),
        'MSE': round(float(mse), 4),
        'RMSE': round(float(rmse), 4),
        'R2': round(float(r2), 4),
        'Adjusted R2': round(float(adj_r2), 4)
    }
