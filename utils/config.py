"""
Vital Sign Project Configuration
Defines colors, directory paths, default target variables, and global constants.
"""

import os

# Visual Theme Colors
PRIMARY_COLOR = "#64E3BF"     # Mint / Teal Accent
SECONDARY_COLOR = "#FFFCBF"   # Soft Yellow / Cream Highlight
BACKGROUND_COLOR = "#F8F9FA"  # Clean Light Background
CARD_BG_COLOR = "#FFFFFF"     # White Card Background
TEXT_COLOR = "#1F2937"        # Dark Gray Body Text

# Project Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ORIGINAL_DATA_DIR = os.path.join(DATA_DIR, "original")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# File Paths
DATASET_CSV = os.path.join(ORIGINAL_DATA_DIR, "diabetic_data.csv")
PREPROCESSED_CSV = os.path.join(PROCESSED_DATA_DIR, "preprocessed_dataset.csv")

PREPROCESSING_REPORT_JSON = os.path.join(REPORTS_DIR, "preprocessing_report.json")
EDA_REPORT_JSON = os.path.join(REPORTS_DIR, "eda_report.json")
MODEL_RESULTS_JSON = os.path.join(REPORTS_DIR, "model_results.json")

# Dataset Defaults
DEFAULT_TARGET_COL = "time_in_hospital"
TARGET_REGRESSION = "time_in_hospital"
TARGET_CLASSIFICATION = "readmitted"
ID_COLUMNS = ["encounter_id", "patient_nbr"]
RANDOM_STATE = 42

# Preprocessing Constants
MISSING_VALUES_REPRESENTATION = ["?", "NaN", "nan", "None", "", "NULL", "null"]
MISSING_DROP_THRESHOLD = 0.70  # Drop columns missing > 70% of entries
