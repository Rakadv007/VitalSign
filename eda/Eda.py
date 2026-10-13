"""
Exploratory Data Analysis (EDA) Module
Calculates structural info, dataset shapes, missing data summaries, duplicates, memory usage,
and statistical summaries for numerical and categorical variables.
"""

import json
import pandas as pd
import numpy as np
from utils.config import EDA_REPORT_JSON, DEFAULT_TARGET_COL


class ExploratoryDataAnalysis:
    def __init__(self, df, target_col=DEFAULT_TARGET_COL):
        self.df = df
        self.target_col = target_col
        self.total_rows, self.total_cols = df.shape
        self.num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
    def get_basic_info(self):
        """
        Returns fundamental structure metadata.
        """
        return {
            'total_rows': self.total_rows,
            'total_cols': self.total_cols,
            'num_cols_count': len(self.num_cols),
            'cat_cols_count': len(self.cat_cols),
            'num_cols': self.num_cols,
            'cat_cols': self.cat_cols,
            'memory_usage_mb': round(self.df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
            'duplicate_rows': int(self.df.duplicated().sum()),
            'duplicate_pct': round((self.df.duplicated().sum() / self.total_rows) * 100, 2)
        }

    def get_statistical_summary(self):
        """
        Calculates describe() stats for numerical columns.
        """
        if not self.num_cols:
            return pd.DataFrame()
        desc = self.df[self.num_cols].describe().T
        desc['skew'] = self.df[self.num_cols].skew().values
        desc['kurtosis'] = self.df[self.num_cols].kurtosis().values
        return desc.round(3)

    def generate_eda_report(self):
        """
        Compiles and saves JSON report of EDA findings.
        """
        info = self.get_basic_info()
        stats = self.get_statistical_summary()
        
        target_dist = {}
        if self.target_col in self.df.columns:
            counts = self.df[self.target_col].value_counts(dropna=False).to_dict()
            target_dist = {str(k): int(v) for k, v in counts.items()}
            
        report = {
            'structure': info,
            'target_col': self.target_col,
            'target_distribution': target_dist,
            'numerical_stats': stats.to_dict() if not stats.empty else {}
        }
        
        with open(EDA_REPORT_JSON, 'w') as f:
            json.dump(report, f, indent=2)
            
        return report
