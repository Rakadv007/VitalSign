"""
Categorical & Target Encoding Module
Dynamically encodes categorical features using One-Hot or Ordinal/Label Encoding.
Encodes target labels safely and maintains mapping lookup dictionary.
"""

from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np


def encode_target(y_series):
    """
    Label encodes target variable and returns encoded series alongside mapping dict.
    """
    le = LabelEncoder()
    y_encoded = le.fit_transform(y_series.astype(str))
    mapping = {int(idx): str(cls) for idx, cls in enumerate(le.classes_)}
    return pd.Series(y_encoded, index=y_series.index, name=y_series.name), mapping, le


def encode_features(X_df, method='onehot', cat_cols=None):
    """
    Encodes categorical features of feature matrix X.
    If method is 'onehot', uses pandas get_dummies (or OneHotEncoder).
    If method is 'label', uses LabelEncoder per categorical feature.
    """
    X_encoded = X_df.copy()
    if cat_cols is None:
        cat_cols = X_encoded.select_dtypes(include=['object', 'category']).columns.tolist()
        
    if not cat_cols:
        return X_encoded, []
        
    encoding_info = []
    
    if method == 'onehot':
        # Drop high-cardinality features like diag codes if unique count > 50 to avoid exploded dummy dimensionality
        high_cardinality = [c for c in cat_cols if X_encoded[c].nunique() > 50]
        for c in high_cardinality:
            # Frequency / top-10 encoding for high-cardinality categories
            top_10 = X_encoded[c].value_counts().nlargest(10).index
            X_encoded[c] = X_encoded[c].apply(lambda val: str(val) if val in top_10 else 'Other')
            encoding_info.append({'feature': c, 'method': 'Top-10 Grouped One-Hot', 'unique_before': X_df[c].nunique()})
            
        X_encoded = pd.get_dummies(X_encoded, columns=cat_cols, drop_first=True, dtype=int)
        # Sanitize column names for tree-based models like XGBoost/LightGBM
        X_encoded.columns = [str(c).replace('[', '_').replace(']', '_').replace('<', 'lt_').replace('>', 'gt_').replace(',', '_') for c in X_encoded.columns]
    else:
        # Ordinal/Label encoding per feature
        for col in cat_cols:
            le = LabelEncoder()
            X_encoded[col] = le.fit_transform(X_encoded[col].astype(str))
            encoding_info.append({'feature': col, 'method': 'Label Encoding', 'classes_count': len(le.classes_)})
            
    return X_encoded, encoding_info
