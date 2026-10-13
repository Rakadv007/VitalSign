"""
Normalization & Scaling Module
Provides fit/transform interface for StandardScaler, MinMaxScaler, and RobustScaler.
Ensures scalers are fit ONLY on training data to prevent data leakage.
"""

from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import pandas as pd
import numpy as np


def get_scaler(method='standard'):
    """
    Factory function for Scikit-Learn feature scalers.
    """
    method = method.lower()
    if method == 'minmax':
        return MinMaxScaler()
    elif method == 'robust':
        return RobustScaler()
    else:
        return StandardScaler()


def scale_numerical_features(X_train, X_test=None, method='standard', num_cols=None):
    """
    Scales numerical features.
    Fits ONLY on X_train, then transforms X_train (and X_test if provided).
    Returns scaled dataframes and scaler object.
    """
    if num_cols is None:
        num_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()
        
    if not num_cols:
        return X_train.copy(), (X_test.copy() if X_test is not None else None), None
        
    scaler = get_scaler(method)
    
    X_train_scaled = X_train.copy()
    X_train_scaled[num_cols] = scaler.fit_transform(X_train[num_cols])
    
    X_test_scaled = None
    if X_test is not None:
        X_test_scaled = X_test.copy()
        X_test_scaled[num_cols] = scaler.transform(X_test[num_cols])
        
    return X_train_scaled, X_test_scaled, scaler
