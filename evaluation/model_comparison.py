"""
Model Comparison & Results Reporting Module
Aggregates performance metrics across all executed supervised models into comparison tables
and interactive comparison bar charts. Saves reports/model_results.json.
"""

import json
import pandas as pd
import numpy as np
import plotly.express as px
from utils.config import MODEL_RESULTS_JSON, PRIMARY_COLOR, SECONDARY_COLOR


def compile_model_comparison(results_list):
    """
    Compiles comparison dataframe and charts for classification or regression tasks.
    """
    applicable_results = [r for r in results_list if r.get('applicable', False)]
    skipped_results = [r for r in results_list if not r.get('applicable', False)]
    
    if not applicable_results:
        return {
            'comparison_table': pd.DataFrame(),
            'skipped_table': pd.DataFrame([{
                'Model': r.get('model_name', 'Unknown'),
                'Status': 'Skipped / Not Applicable',
                'Reason': r.get('reason', 'N/A')
            } for r in skipped_results]),
            'charts': {}
        }
        
    task_type = applicable_results[0].get('task_type', 'classification')
    
    rows = []
    for r in applicable_results:
        model_name = r.get('model_name', 'Unknown')
        metrics = r.get('metrics', {})
        row = {'Model': model_name}
        row.update(metrics)
        rows.append(row)
        
    comp_df = pd.DataFrame(rows)
    
    skipped_rows = [{
        'Model': r.get('model_name', 'Unknown'),
        'Status': 'Skipped / Not Applicable',
        'Reason': r.get('reason', 'N/A')
    } for r in skipped_results]
    skipped_df = pd.DataFrame(skipped_rows)
    
    charts = {}
    if task_type == 'classification':
        if 'Accuracy' in comp_df.columns:
            charts['accuracy_fig'] = px.bar(
                comp_df, x='Model', y='Accuracy', text='Accuracy',
                color='Accuracy', color_continuous_scale=[SECONDARY_COLOR, PRIMARY_COLOR],
                title="Model Accuracy Comparison"
            )
            charts['accuracy_fig'].update_traces(texttemplate='%{text:.4f}', textposition='outside')
            charts['accuracy_fig'].update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            
        metric_col = 'F1-Score' if 'F1-Score' in comp_df.columns else 'F1-Score (Macro)'
        if metric_col in comp_df.columns:
            charts['f1_fig'] = px.bar(
                comp_df, x='Model', y=metric_col, text=metric_col,
                color=metric_col, color_continuous_scale=[SECONDARY_COLOR, PRIMARY_COLOR],
                title="Model F1-Score Comparison"
            )
            charts['f1_fig'].update_traces(texttemplate='%{text:.4f}', textposition='outside')
            charts['f1_fig'].update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    else:
        if 'R2' in comp_df.columns:
            charts['r2_fig'] = px.bar(
                comp_df, x='Model', y='R2', text='R2',
                color='R2', color_continuous_scale=[SECONDARY_COLOR, PRIMARY_COLOR],
                title="Model R² Score Comparison"
            )
            charts['r2_fig'].update_traces(texttemplate='%{text:.4f}', textposition='outside')
            charts['r2_fig'].update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            
        if 'RMSE' in comp_df.columns:
            charts['rmse_fig'] = px.bar(
                comp_df, x='Model', y='RMSE', text='RMSE',
                color='RMSE', color_continuous_scale=['#F87171', SECONDARY_COLOR],
                title="Model RMSE Comparison (Lower is Better)"
            )
            charts['rmse_fig'].update_traces(texttemplate='%{text:.4f}', textposition='outside')
            charts['rmse_fig'].update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            
    # Save model results JSON report
    report_data = {
        'task_type': task_type,
        'models_evaluated': [r.get('model_name') for r in applicable_results],
        'models_skipped': skipped_rows,
        'metrics_summary': comp_df.to_dict(orient='records')
    }
    
    with open(MODEL_RESULTS_JSON, 'w') as f:
        json.dump(report_data, f, indent=2)
        
    return {
        'task_type': task_type,
        'comparison_table': comp_df,
        'skipped_table': skipped_df,
        'charts': charts
    }
