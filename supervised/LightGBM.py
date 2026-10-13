"""
LightGBM Module
Implements LGBMClassifier and LGBMRegressor using the lightgbm library.
Reports dependency status cleanly if unavailable.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix,
    mean_absolute_error, mean_squared_error, r2_score
)
from preprocessing.Normalization import scale_numerical_features
from utils.config import RANDOM_STATE

try:
    from lightgbm import LGBMClassifier, LGBMRegressor
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False


def run_lightgbm(df, target_col='readmitted', n_estimators=50, learning_rate=0.1, max_depth=5):
    """
    Trains LightGBM model for classification or regression.
    """
    if not LIGHTGBM_AVAILABLE:
        return {
            'applicable': False,
            'model_name': 'LightGBM',
            'reason': "LightGBM library is not installed in the environment."
        }
        
    if target_col not in df.columns:
        return {'applicable': False, 'reason': f"Target column '{target_col}' not found."}
        
    y = df[target_col].copy()
    is_numeric = pd.api.types.is_numeric_dtype(y)
    unique_vals = y.nunique()
    is_continuous = is_numeric and (unique_vals > 5 or target_col == 'time_in_hospital')
    
    # Binary classification target mapping if 3 classes present
    if not is_continuous and unique_vals == 3:
        y = y.apply(lambda v: 0 if str(v).strip().upper() in ['NO', '2'] else 1)
        unique_vals = 2
    
    drop_cols = [c for c in ['readmitted', 'time_in_hospital', 'encounter_id', 'patient_nbr'] if c in df.columns]
    X = df.drop(columns=drop_cols)
    
    if is_continuous:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)
        X_train_scaled, X_test_scaled, _ = scale_numerical_features(X_train, X_test, method='standard')
        
        model = LGBMRegressor(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            random_state=RANDOM_STATE,
            verbosity=-1,
            n_jobs=-1
        )
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        
        mae = float(mean_absolute_error(y_test, y_pred))
        mse = float(mean_squared_error(y_test, y_pred))
        rmse = float(np.sqrt(mse))
        r2 = float(r2_score(y_test, y_pred))
        
        return {
            'applicable': True,
            'model_name': 'LightGBM Regressor',
            'task_type': 'regression',
            'metrics': {'MAE': round(mae, 4), 'MSE': round(mse, 4), 'RMSE': round(rmse, 4), 'R2': round(r2, 4)},
            'y_test': y_test.values,
            'y_pred': y_pred
        }
    else:
        unq_classes = sorted(np.unique(y))
        class_to_idx = {cls: idx for idx, cls in enumerate(unq_classes)}
        y_idx = y.map(class_to_idx)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y_idx, test_size=0.2, random_state=RANDOM_STATE, stratify=y_idx)
        X_train_scaled, X_test_scaled, _ = scale_numerical_features(X_train, X_test, method='standard')
        
        model = LGBMClassifier(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            random_state=RANDOM_STATE,
            verbosity=-1,
            n_jobs=-1
        )
        model.fit(X_train_scaled, y_train)
        y_pred_idx = model.predict(X_test_scaled)
        
        acc = accuracy_score(y_test, y_pred_idx)
        prec_macro = precision_score(y_test, y_pred_idx, average='macro', zero_division=0)
        rec_macro = recall_score(y_test, y_pred_idx, average='macro', zero_division=0)
        f1_macro = f1_score(y_test, y_pred_idx, average='macro', zero_division=0)
        f1_weighted = f1_score(y_test, y_pred_idx, average='weighted', zero_division=0)
        
        roc_auc = 0.0
        if hasattr(model, "predict_proba"):
            y_proba = model.predict_proba(X_test_scaled)
            if len(unq_classes) == 2:
                roc_auc = roc_auc_score(y_test, y_proba[:, 1])
            else:
                try:
                    roc_auc = roc_auc_score(y_test, y_proba, multi_class='ovr', average='macro')
                except Exception:
                    roc_auc = 0.0
                    
        cm = confusion_matrix(y_test, y_pred_idx)
        labels = [str(c) for c in unq_classes]
        
        imp_df = pd.DataFrame({
            'Feature': X.columns,
            'Importance': model.feature_importances_
        }).sort_values(by='Importance', ascending=False).reset_index(drop=True)
        
        return {
            'applicable': True,
            'model_name': 'LightGBM Classifier',
            'task_type': 'classification',
            'metrics': {
                'Accuracy': round(float(acc), 4),
                'Precision': round(float(prec_macro), 4),
                'Recall': round(float(rec_macro), 4),
                'F1-Score': round(float(f1_macro), 4),
                'F1-Score (Weighted)': round(float(f1_weighted), 4),
                'ROC-AUC': round(float(roc_auc), 4)
            },
            'y_test': y_test.values,
            'y_pred': y_pred_idx,
            'confusion_matrix': cm,
            'labels': labels,
            'feature_importance': imp_df
        }
