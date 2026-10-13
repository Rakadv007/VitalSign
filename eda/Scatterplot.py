"""
Bivariate Scatterplot & Regression Analysis Module
Generates interactive scatterplots with OLS regression trendlines and Pearson correlation values.
"""

import pandas as pd
import numpy as np
from scipy import stats
from utils.plotting import create_scatter_regression_fig


def generate_scatterplot(df, x_col, y_col):
    """
    Calculates correlation coefficient and produces interactive scatterplot figure.
    """
    valid_data = df[[x_col, y_col]].dropna()
    if len(valid_data) == 0:
        return None, 0.0
        
    r_val, p_val = stats.pearsonr(valid_data[x_col], valid_data[y_col])
    fig = create_scatter_regression_fig(df, x_col, y_col, corr_val=r_val)
    return fig, round(float(r_val), 3)
