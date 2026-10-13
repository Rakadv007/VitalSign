"""
Multinomial Logistic Regression Module
Designed for multiclass target variables (>2 classes).
Calculates macro and weighted classification metrics and confusion matrix.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from preprocessing.Normalization import scale_numerical_features
from utils.config import RANDOM_STATE


def run_multinomial_logistic_regression(df, target_col='readmitted', C=1.0, solver='lbfgs'):
    """
    Trains Multinomial Logistic Regression model for multiclass targets.
    """
    if target_col not in df.columns:
        return {'applicable': False, 'reason': f"Target column '{target_col}' not found."}
        
    y = df[target_col]
    is_numeric = pd.api.types.is_numeric_dtype(y)
    unique_classes = y.nunique()
    
    # Check if target is continuous numerical
    if is_numeric and unique_classes > 20:
        return {
            'applicable': False,
            'model_name': 'Multinomial Logistic Regression',
            'reason': f"Multinomial Logistic Regression skipped: Target '{target_col}' is continuous numerical. Logistic Regression requires categorical target."
        }
        
    # Train/Test Split
    X = df.drop(columns=[target_col])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y)
    
    # Scale features
    X_train_scaled, X_test_scaled, scaler = scale_numerical_features(X_train, X_test, method='standard')
    
    model = LogisticRegression(
        C=C,
        solver=solver,
        max_iter=1000,
        random_state=RANDOM_STATE
    )
    model.fit(X_train_scaled, y_train)
    
    y_pred = model.predict(X_test_scaled)
    
    # Predict probabilities for ROC-AUC
    y_proba = model.predict_proba(X_test_scaled) if hasattr(model, "predict_proba") else None
    
    acc = accuracy_score(y_test, y_pred)
    prec_macro = precision_score(y_test, y_pred, average='macro', zero_division=0)
    rec_macro = recall_score(y_test, y_pred, average='macro', zero_division=0)
    f1_macro = f1_score(y_test, y_pred, average='macro', zero_division=0)
    
    f1_weighted = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    roc_auc = 0.0
    if y_proba is not None and len(np.unique(y_test)) > 1:
        try:
            roc_auc = roc_auc_score(y_test, y_proba, multi_class='ovr', average='macro')
        except Exception:
            roc_auc = 0.0
            
    cm = confusion_matrix(y_test, y_pred)
    
    metrics = {
        'Accuracy': round(float(acc), 4),
        'Precision': round(float(prec_macro), 4),
        'Recall': round(float(rec_macro), 4),
        'F1-Score': round(float(f1_macro), 4),
        'F1-Score (Weighted)': round(float(f1_weighted), 4),
        'ROC-AUC': round(float(roc_auc), 4)
    }
    
    labels = [str(c) for c in sorted(np.unique(y))]
    
    return {
        'applicable': True,
        'model_name': 'Multinomial Logistic Regression',
        'task_type': 'classification',
        'metrics': metrics,
        'y_test': y_test.values,
        'y_pred': y_pred,
        'confusion_matrix': cm,
        'labels': labels,
        'best_params': {'C': C, 'solver': solver}
    }
