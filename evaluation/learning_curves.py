"""
Learning Curves Module
Uses sklearn.model_selection.learning_curve to compute training and validation scores across sample sizes.
Produces Plotly learning curve figures.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.model_selection import learning_curve
from preprocessing.Normalization import scale_numerical_features
from utils.config import RANDOM_STATE, PRIMARY_COLOR, SECONDARY_COLOR


from sklearn.base import is_classifier, is_regressor


def generate_learning_curve(model, X, y, scoring=None, train_sizes=np.linspace(0.2, 1.0, 5), cv=3):
    """
    Computes learning curve data and returns Plotly figure.
    """
    try:
        # Dynamically determine appropriate scoring metric if unspecified
        if scoring is None or scoring == 'accuracy':
            if is_regressor(model):
                scoring = 'r2'
            else:
                scoring = 'accuracy'
                
        # Scale numerical features safely
        X_scaled, _, _ = scale_numerical_features(X)
        
        # Ensure y is numeric if categorical labels are provided
        if is_classifier(model) and not pd.api.types.is_numeric_dtype(y):
            from sklearn.preprocessing import LabelEncoder
            y = LabelEncoder().fit_transform(y.astype(str))
        
        train_sizes_abs, train_scores, val_scores, *_ = learning_curve(
            estimator=model,
            X=X_scaled,
            y=y,
            train_sizes=train_sizes,
            cv=cv,
            scoring=scoring,
            shuffle=True,
            random_state=RANDOM_STATE,
            n_jobs=-1
        )
        
        train_mean = np.mean(train_scores, axis=1)
        train_std = np.std(train_scores, axis=1)
        val_mean = np.mean(val_scores, axis=1)
        val_std = np.std(val_scores, axis=1)
        
        fig = go.Figure()
        
        # Training Score Trace
        fig.add_trace(go.Scatter(
            x=train_sizes_abs,
            y=train_mean,
            mode='lines+markers',
            name='Training Score',
            line=dict(color=PRIMARY_COLOR, width=3)
        ))
        
        # Validation Score Trace
        fig.add_trace(go.Scatter(
            x=train_sizes_abs,
            y=val_mean,
            mode='lines+markers',
            name='Validation Score',
            line=dict(color='#F59E0B', width=3, dash='dash')
        ))
        
        fig.update_layout(
            title=f"Model Learning Curve (Metric: {scoring})",
            xaxis_title="Training Set Size (Samples)",
            yaxis_title="Score",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        curve_df = pd.DataFrame({
            'Train Sample Size': train_sizes_abs,
            'Train Score Mean': np.round(train_mean, 4),
            'Validation Score Mean': np.round(val_mean, 4)
        })
        
        return {
            'applicable': True,
            'fig': fig,
            'curve_table': curve_df
        }
    except Exception as e:
        return {
            'applicable': False,
            'reason': f"Could not generate learning curve: {str(e)}"
        }
