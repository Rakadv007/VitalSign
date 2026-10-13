# Vital Sign — Machine Learning Dashboard

**Vital Sign** is a production-grade, interactive Machine Learning dashboard built in Python using Streamlit, Scikit-Learn, XGBoost, LightGBM, and Plotly. It performs end-to-end data processing, exploratory data analysis (EDA), supervised classification and regression, unsupervised clustering, anomaly detection, dimensionality reduction, learning curve analysis, and unified model comparison.

---

## 🎨 Theme & Visual Palette

- **Primary Accent Color**: `#64E3BF` (Mint / Teal)
- **Secondary Highlight Color**: `#FFFCBF` (Soft Yellow / Cream)

---

## 📊 Features

### 1. Main Menu
- **Dashboard**: Dynamic dataset summary, row/column dimensions, memory usage, dual target distribution (readmission 2-class & length of stay 1-14 days), and interactive dataset preview (`df.head(10)`) with column filter.
- **Preprocessing**: Missing value analysis & imputation (mode/median), outlier detection (IQR) & Winsorization/capping, normalizer factory (StandardScaler, MinMaxScaler, RobustScaler), and categorical/target encoding.
- **EDA**: 8-section interactive dashboard covering data loading & structure, missing values & duplicate analysis, dual target distributions, numerical histograms/KDE curves, 1.5×IQR outlier boxplots, full Pearson correlation matrix heatmap, bivariate regression scatter plots with OLS trendlines, and categorical frequency bar charts.

### 2. Supervised Learning
- **Target 1: Length of Stay (`time_in_hospital`) — Continuous Regression**:
  - **Linear Regression**: MAE: 1.8111, MSE: 5.6826, RMSE: 2.3838, R²: 0.3471, Adjusted R²: 0.3429
  - **Random Forest Regressor**: MAE: 1.7429, MSE: 5.3516, RMSE: 2.3134, R²: 0.3852
  - **AdaBoost Regressor**: MAE: 2.1861, MSE: 6.9484, RMSE: 2.6360, R²: 0.2017
  - **Gradient Boosting Regressor**: MAE: 1.7322, MSE: 5.2516, RMSE: 2.2916, R²: 0.3966
  - **XGBoost Regressor**: MAE: 1.7295, MSE: 5.2441, RMSE: 2.2900, R²: 0.3975
  - **LightGBM Regressor**: MAE: 1.7312, MSE: 5.2539, RMSE: 2.2921, R²: 0.3964
- **Target 2: Readmission Risk (`readmitted`) — Binary 2-Class Classification (NO vs Readmitted)**:
  - **Logistic Regression**: Accuracy: 0.6295, Precision: 0.6399, Recall: 0.4485, F1: 0.5274, ROC-AUC: 0.6663
  - **Random Forest Classifier**: Accuracy: 0.6394, Precision: 0.6532, Recall: 0.4640, F1: 0.5426, ROC-AUC: 0.6862
  - **AdaBoost Classifier**: Accuracy: 0.6292, Precision: 0.6339, Recall: 0.4627, F1: 0.5350, ROC-AUC: 0.6725
  - **Gradient Boosting Classifier**: Accuracy: 0.6409, Precision: 0.6394, Recall: 0.5067, F1: 0.5653, ROC-AUC: 0.6973
  - **XGBoost Classifier**: Accuracy: 0.6416, Precision: 0.6408, Recall: 0.5062, F1: 0.5656, ROC-AUC: 0.6977
  - **LightGBM Classifier**: Accuracy: 0.6418, Precision: 0.6402, Recall: 0.5089, F1: 0.5671, ROC-AUC: 0.6973
- **Interactive UI**: Every model is rendered as an interactive card with real-time 3D tilt on hover and click-to-expand modal details.

### 3. Unsupervised Learning
- **Clustering**: K-Means with Elbow curve (inertia) and peak Silhouette score (K=3); Hierarchical Agglomerative Clustering (Ward linkage); DBSCAN with density and noise analysis.
- **Anomaly Detection**: Isolation Forest outlier detection (5.0% contamination rate, 5,088 anomalies flagged).
- **Dimensionality Reduction**: Principal Component Analysis (PCA) with scree plot, cumulative variance (68.4% across 10 PCs), and 2D/3D projections.

### 4. Metrics & Evaluation
- **Supervised Regression Metrics**: MAE, MSE, RMSE, R², Adjusted R².
- **Supervised Classification Metrics**: Accuracy, Precision, Recall, F1-Score, ROC-AUC, Confusion Matrix.
- **Unsupervised Metrics**: Silhouette Score (0.185), Calinski-Harabasz Index (1428.5), Davies-Bouldin Index (1.642).
- **Learning Curves**: Sample size progression evaluating training vs validation generalization.

---

## 📁 Project Structure

```text
Vital_Sign/
│
├── app.py                      # Main Streamlit Dashboard Application
├── requirements.txt            # Python Dependencies
├── README.md                   # Documentation
│
├── data/
│   ├── original/
│   │   └── diabetic_data.csv   # Raw Dataset (Diabetes 130-US Hospitals)
│   └── processed/
│       └── preprocessed_dataset.csv  # Preprocessed Feature Dataset
│
├── preprocessing/
│   ├── __init__.py
│   ├── Outlier.py              # IQR Detection & Winsorization
│   ├── Normalization.py        # Scaler Factory (Standard, MinMax, Robust)
│   ├── Missing_Values.py       # Imputation & Missing Analysis
│   └── Encoding.py             # Categorical & Target Label Encoding
│
├── eda/
│   ├── __init__.py
│   ├── Eda.py                  # Structure Metadata & Summary Stats
│   ├── EDA_output.py           # Target Distribution & Class Imbalance
│   ├── Heat_map.py             # Correlation Matrices
│   ├── Scatterplot.py          # Scatterplots & OLS Regression
│   ├── Boxplots.py             # Boxplots & Distribution Curves
│   └── Correlation_Heatmaps.py # Top Collinear Pairs
│
├── supervised/
│   ├── __init__.py
│   ├── Linear_Regression.py    # Baseline, Ridge, Lasso, ElasticNet
│   ├── Logistic_Regression.py  # Binary Logistic Regression
│   ├── Multinomial_Logistic_Regression.py # Multiclass Logistic Regression
│   ├── Random_Forest.py        # Random Forest Classifier & Regressor
│   ├── Bagging.py              # Bagging Classifier & Regressor
│   ├── AdaBoost.py             # AdaBoost Classifier & Regressor
│   ├── Gradient_Boost.py       # Gradient Boosting Classifier & Regressor
│   ├── XGBoost.py              # XGBoost Classifier & Regressor
│   └── LightGBM.py             # LightGBM Classifier & Regressor
│
├── unsupervised/
│   ├── __init__.py
│   ├── KMeans.py               # K-Means & Elbow Curve
│   ├── Hierarchical_Clustering.py # Agglomerative & Dendrogram
│   ├── DBSCAN.py               # DBSCAN & Noise Analysis
│   ├── Anomaly_Detection.py    # Isolation Forest Anomaly Detection
│   └── Dimensionality_Reduction.py # PCA (Scree Plot, 2D & 3D)
│
├── evaluation/
│   ├── __init__.py
│   ├── supervised_metrics.py   # Classification & Regression Metrics
│   ├── unsupervised_metrics.py # Silhouette, Calinski-Harabasz, Davies-Bouldin
│   ├── learning_curves.py      # Cross-validation Learning Curves
│   └── model_comparison.py     # Comparison Tables & Visualizations
│
├── reports/
│   ├── preprocessing_report.json # Preprocessing Log & Metadata
│   ├── eda_report.json         # EDA Findings Report
│   └── model_results.json      # Model Performance Comparison Report
│
└── utils/
    ├── __init__.py
    ├── data_loader.py          # Data Loading & Overview Utilities
    ├── config.py               # Project Colors, Paths, and Constants
    └── plotting.py             # Plotly & Seaborn Theme Styling
```

---

## ⚡ Installation & Setup

1. **Clone or navigate to the repository directory**:
   ```bash
   cd VitalSign
   ```

2. **Install Required Python Packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Dataset Location**:
   Ensure the raw dataset is placed at `data/original/diabetic_data.csv`.

4. **Launch Dashboard locally**:
   ```bash
   python app.py
   ```
   Open `http://localhost:8000` in your web browser.

---

## 🐳 Docker Deployment

### Option A: Using Docker Compose (Recommended)
```bash
docker compose up --build
```
Access the dashboard at `http://localhost:8000`.

### Option B: Using Docker CLI
1. **Build the Docker Image**:
   ```bash
   docker build -t vitalsign .
   ```

2. **Run the Container**:
   ```bash
   docker run -d -p 8000:8000 --name vitalsign-app vitalsign
   ```
   Open `http://localhost:8000` in your browser.

3. **Run Individual Machine Learning Scripts (Optional)**:
   ```bash
   docker run --rm vitalsign python supervised/Logistic_Regression.py
   ```

4. **Stop the Container**:
   ```bash
   docker stop vitalsign-app
   ```

---

## 🔒 Data Integrity & Reproducibility Guarantee

1. **100% Real Calculations**: Zero synthetic, placeholder, or manually hard-coded metrics/charts. Every figure and number is computed directly from `diabetic_data.csv` or fitted ML pipelines.
2. **Data Leakage Prevention**: All feature scaling, imputation, and encoding transformers are fitted exclusively on the training split (`X_train`) during model evaluation.
3. **Dynamic Model Validity**: Models validate target data types automatically. If an algorithm is mathematically incompatible (e.g. Linear Regression on categorical readmission target), it is safely skipped with a detailed scientific rationale displayed on the dashboard.
