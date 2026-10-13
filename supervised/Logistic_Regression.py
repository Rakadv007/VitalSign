"""
Binary Logistic Regression Module
Applicable ONLY when target has exactly two classes.
Returns explicit skip status and guidance if target has >2 classes.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from preprocessing.Normalization import scale_numerical_features
from utils.config import RANDOM_STATE


def run_binary_logistic_regression(df, target_col='readmitted', C=1.0, penalty='l2', solver='lbfgs'):
    """
    Trains Binary Logistic Regression if target unique classes == 2.
    """
    if target_col not in df.columns:
        return {'applicable': False, 'reason': f"Target column '{target_col}' not found."}
        
    y = df[target_col].copy()
    unique_classes = y.nunique()
    
    # If 3 classes present in readmitted, convert to binary 2 classes (0: NO, 1: Readmitted)
    if unique_classes == 3:
        y = y.apply(lambda v: 0 if str(v).strip().upper() in ['NO', '2'] else 1)
        unique_classes = 2
    
    if unique_classes != 2:
        return {
            'applicable': False,
            'model_name': 'Binary Logistic Regression',
            'reason': f"Binary Logistic Regression skipped: Target '{target_col}' contains {unique_classes} classes. Binary Logistic Regression requires exactly 2 classes."
        }
        
    # Train/Test Split (drop leaking target and ID columns)
    drop_cols = [c for c in ['readmitted', 'time_in_hospital', 'encounter_id', 'patient_nbr'] if c in df.columns]
    X = df.drop(columns=drop_cols)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y)
    
    # Scale features
    X_train_scaled, X_test_scaled, scaler = scale_numerical_features(X_train, X_test, method='standard')
    
    model = LogisticRegression(C=C, penalty=penalty, solver=solver, max_iter=1000, random_state=RANDOM_STATE)
    model.fit(X_train_scaled, y_train)
    
    y_pred = model.predict(X_test_scaled)
    y_proba = model.predict_proba(X_test_scaled)[:, 1] if hasattr(model, "predict_proba") else None
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='binary', zero_division=0)
    rec = recall_score(y_test, y_pred, average='binary', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='binary', zero_division=0)
    roc_auc = roc_auc_score(y_test, y_proba) if y_proba is not None else 0.0
    cm = confusion_matrix(y_test, y_pred)
    
    metrics = {
        'Accuracy': round(float(acc), 4),
        'Precision': round(float(prec), 4),
        'Recall': round(float(rec), 4),
        'F1-Score': round(float(f1), 4),
        'ROC-AUC': round(float(roc_auc), 4)
    }
    
    return {
        'applicable': True,
        'model_name': 'Binary Logistic Regression',
        'task_type': 'classification',
        'metrics': metrics,
        'y_test': y_test.values,
        'y_pred': y_pred,
        'confusion_matrix': cm,
        'labels': [str(c) for c in np.unique(y)]
    }
