"""
Linear Regression Module (Baseline, Ridge, Lasso, ElasticNet)
Applicable ONLY when target variable is continuous numerical.
Dynamically validates target type and reports reason if skipped.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from preprocessing.Normalization import scale_numerical_features
from utils.config import RANDOM_STATE


def run_linear_regression(df, target_col='time_in_hospital', model_type='Baseline'):
    """
    Trains and evaluates Linear Regression models on continuous numerical target.
    """
    # 1. Target Validation
    if target_col not in df.columns:
        return {'applicable': False, 'reason': f"Target column '{target_col}' not found in dataset."}
        
    y = df[target_col]
    is_numeric = pd.api.types.is_numeric_dtype(y)
    unique_vals = y.nunique()
    
    # Check if target is continuous numerical
    if not (is_numeric and (unique_vals > 5 or target_col == 'time_in_hospital')):
        return {
            'applicable': False,
            'model_name': f"Linear Regression ({model_type})",
            'reason': f"Linear Regression skipped: Target '{target_col}' is categorical ({unique_vals} unique classes). Linear Regression requires a continuous numerical target feature."
        }
        
    # 2. Train/Test Split & Preprocessing (No Leakage)
    drop_cols = [c for c in [target_col, 'readmitted', 'encounter_id', 'patient_nbr'] if c in df.columns]
    X = df.drop(columns=drop_cols)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)
    
    # Scale features (fit ONLY on X_train)
    X_train_scaled, X_test_scaled, scaler = scale_numerical_features(X_train, X_test, method='standard')
    
    # 3. Model Selection
    model_type = model_type.lower()
    if model_type == 'ridge':
        model = Ridge(alpha=1.0, random_state=RANDOM_STATE)
    elif model_type == 'lasso':
        model = Lasso(alpha=0.1, random_state=RANDOM_STATE)
    elif model_type == 'elasticnet':
        model = ElasticNet(alpha=0.1, l1_ratio=0.5, random_state=RANDOM_STATE)
    else:
        model = LinearRegression()
        
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    
    # 4. Metrics
    mae = float(mean_absolute_error(y_test, y_pred))
    mse = float(mean_squared_error(y_test, y_pred))
    rmse = float(np.sqrt(mse))
    r2 = float(r2_score(y_test, y_pred))
    
    n = len(y_test)
    p = X_train_scaled.shape[1]
    adj_r2 = float(1 - (1 - r2) * (n - 1) / (n - p - 1)) if (n - p - 1) > 0 else r2
    
    metrics = {
        'MAE': round(mae, 4),
        'MSE': round(mse, 4),
        'RMSE': round(rmse, 4),
        'R2': round(r2, 4),
        'Adjusted_R2': round(adj_r2, 4)
    }
    
    # Residuals
    residuals = y_test.values - y_pred
    
    return {
        'applicable': True,
        'model_name': f"Linear Regression ({model_type.capitalize()})",
        'task_type': 'regression',
        'metrics': metrics,
        'y_test': y_test.values,
        'y_pred': y_pred,
        'residuals': residuals,
        'model_object': model
    }
