"""
Numerical Boxplot & Outlier Visualization Module
Generates distribution and boxplot charts for numerical variables.
"""

import pandas as pd
import numpy as np
from utils.plotting import create_feature_distribution_fig


def generate_feature_boxplot(df, feature_name):
    """
    Renders histogram and boxplot for selected feature.
    """
    if feature_name not in df.columns:
        return None
    return create_feature_distribution_fig(df, feature_name)
