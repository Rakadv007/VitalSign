"""
Vital Sign Custom Plotting Utility
Provides consistent, modern, clean visualization builders for Plotly & Seaborn.
Uses project primary color #64E3BF (Mint/Teal) and secondary color #FFFCBF (Soft Yellow).
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from utils.config import PRIMARY_COLOR, SECONDARY_COLOR, TEXT_COLOR

# Set default Seaborn style
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = 'Inter, Roboto, sans-serif'
plt.rcParams['axes.edgecolor'] = '#E5E7EB'
plt.rcParams['axes.linewidth'] = 1.0


def create_target_distribution_chart(target_dist_df, title="Target Class Distribution"):
    """
    Returns an interactive Plotly bar chart for target distribution.
    """
    fig = px.bar(
        target_dist_df,
        x='Target Value',
        y='Count',
        text='Percentage (%)',
        color_discrete_sequence=[PRIMARY_COLOR],
        title=title
    )
    fig.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside',
        marker_line_color='#34D399',
        marker_line_width=1.5
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXT_COLOR, size=13),
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title="Target Value",
        yaxis_title="Count"
    )
    return fig


def create_feature_distribution_fig(df, feature_name):
    """
    Returns a histogram + KDE plot using Plotly for a numerical feature.
    """
    fig = px.histogram(
        df,
        x=feature_name,
        marginal="box",
        nbins=30,
        color_discrete_sequence=[PRIMARY_COLOR],
        title=f"Distribution & Boxplot of {feature_name}"
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXT_COLOR),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig


def create_correlation_heatmap_fig(corr_df, title="Feature Correlation Heatmap"):
    """
    Returns an interactive Plotly Heatmap for correlation matrices.
    """
    fig = px.imshow(
        corr_df,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale=[[0, "#E0F2FE"], [0.5, SECONDARY_COLOR], [1, PRIMARY_COLOR]],
        title=title
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXT_COLOR, size=11),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig


def create_scatter_regression_fig(df, x_col, y_col, corr_val=None):
    """
    Returns a scatter plot with regression line for feature pairs.
    """
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        trendline="ols",
        trendline_color_override="#10B981",
        color_discrete_sequence=[PRIMARY_COLOR],
        title=f"{x_col} vs {y_col} (Correlation: {corr_val:.3f})" if corr_val is not None else f"{x_col} vs {y_col}"
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXT_COLOR),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig


def create_confusion_matrix_fig(cm, labels, title="Confusion Matrix"):
    """
    Renders a confusion matrix heatmap using Plotly.
    """
    fig = px.imshow(
        cm,
        x=labels,
        y=labels,
        text_auto=True,
        color_continuous_scale=[[0, "#F1F5F9"], [1, PRIMARY_COLOR]],
        title=title,
        labels=dict(x="Predicted Label", y="Actual Label", color="Count")
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXT_COLOR),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig


def create_feature_importance_fig(importance_df, title="Top Feature Importances"):
    """
    Renders horizontal bar chart of feature importances.
    """
    fig = px.bar(
        importance_df.head(15),
        x='Importance',
        y='Feature',
        orientation='h',
        color='Importance',
        color_continuous_scale=[SECONDARY_COLOR, PRIMARY_COLOR],
        title=title
    )
    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXT_COLOR),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig
