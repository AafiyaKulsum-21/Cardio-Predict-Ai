"""
Data Preprocessing Module for CardioPredict AI.
Handles data ingestion, validation, splitting, and feature scaling.
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

FEATURE_NAMES = [
    'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
    'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
]
TARGET_NAME = 'target'


def load_dataset(file_path: str = 'data/heart.csv') -> pd.DataFrame:
    """Loads heart disease dataset from CSV file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset file not found at: {file_path}")
    df = pd.read_csv(file_path)
    return df


def validate_and_clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validates schema, checks missing values, and cleans dataframe."""
    df_clean = df.copy()
    
    # Verify required columns exist
    missing_cols = [c for c in FEATURE_NAMES + [TARGET_NAME] if c not in df_clean.columns]
    if missing_cols:
        raise ValueError(f"Dataset missing required columns: {missing_cols}")
    
    # Handle missing values if any
    if df_clean.isnull().sum().sum() > 0:
        df_clean = df_clean.dropna()
        
    # Drop duplicates if present
    df_clean = df_clean.drop_duplicates().reset_index(drop=True)
    
    return df_clean


def prepare_train_test_data(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42):
    """
    Splits features and target into stratified train and test sets,
    and applies standard scaling to numerical features.
    """
    X = df[FEATURE_NAMES]
    y = df[TARGET_NAME]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return (
        X_train, X_test, y_train, y_test,
        X_train_scaled, X_test_scaled, scaler
    )


def save_scaler(scaler, output_path: str = 'models/scaler.joblib'):
    """Serializes the fitted scaler to disk using Joblib."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    joblib.dump(scaler, output_path)
    print(f"[INFO] Scaler saved successfully to {output_path}")


def load_scaler(input_path: str = 'models/scaler.joblib'):
    """Loads a previously serialized scaler."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Scaler file not found at: {input_path}")
    return joblib.load(input_path)


if __name__ == '__main__':
    data = load_dataset()
    cleaned = validate_and_clean_data(data)
    print(f"[INFO] Cleaned dataset shape: {cleaned.shape}")
    X_tr, X_te, y_tr, y_te, X_tr_sc, X_te_sc, sc = prepare_train_test_data(cleaned)
    save_scaler(sc)
    print(f"[INFO] Train samples: {X_tr.shape[0]}, Test samples: {X_te.shape[0]}")
