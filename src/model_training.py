"""
Model Training and Serialization Module for CardioPredict AI.
Trains and compares multiple classifiers, tunes hyperparameters, evaluates performance,
generates diagnostic charts, and serializes artifacts via Joblib & Pickle.
Target convention:
    1 = Heart Disease / High Risk
    0 = Healthy / Low Risk
"""

import os
import json
import pickle
import joblib
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, roc_curve, classification_report
)

from src.data_preprocessing import (
    load_dataset, validate_and_clean_data,
    prepare_train_test_data, save_scaler, FEATURE_NAMES
)

warnings.filterwarnings('ignore', category=FutureWarning)

# Configure plot styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'


def train_and_compare_models(X_train_scaled, y_train, X_test_scaled, y_test):
    """
    Trains multiple baseline models, performs 5-fold cross-validation,
    evaluates on the holdout test set, and returns comparison records.
    """
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Support Vector Machine': SVC(probability=True, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42),
        'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5)
    }

    results = []
    trained_models = {}

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    for name, model in models.items():
        # Cross-validation on training data
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring='f1')
        
        # Fit on full training set
        model.fit(X_train_scaled, y_train)
        trained_models[name] = model

        # Evaluate on test set
        y_pred = model.predict(X_test_scaled)
        y_prob = model.predict_proba(X_test_scaled)[:, 1] if hasattr(model, 'predict_proba') else y_pred

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc = roc_auc_score(y_test, y_prob)

        results.append({
            'Model': name,
            'CV_F1_Mean': float(np.mean(cv_scores)),
            'CV_F1_Std': float(np.std(cv_scores)),
            'Accuracy': float(acc),
            'Precision': float(prec),
            'Recall': float(rec),
            'F1_Score': float(f1),
            'ROC_AUC': float(roc)
        })

    df_results = pd.DataFrame(results).sort_values(by='F1_Score', ascending=False)
    return df_results, trained_models


def tune_best_model(X_train_scaled, y_train):
    """
    Performs grid search hyperparameter tuning for Random Forest Classifier
    to maximize clinical recall and F1-score for heart disease detection.
    """
    param_grid = {
        'n_estimators': [100, 150, 200],
        'max_depth': [None, 4, 6, 8],
        'min_samples_split': [2, 4, 6],
        'min_samples_leaf': [1, 2, 3],
        'class_weight': ['balanced', None]
    }
    
    rf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(
        rf, param_grid, cv=5, scoring='f1', n_jobs=-1, verbose=0
    )
    grid_search.fit(X_train_scaled, y_train)

    print(f"[INFO] Best Parameters: {grid_search.best_params_}")
    print(f"[INFO] Best CV F1-Score: {grid_search.best_score_:.4f}")
    return grid_search.best_estimator_, grid_search.best_params_


def generate_evaluation_visualizations(model, model_name, df_results, X_test_scaled, y_test, output_dir='reports/plots'):
    """Generates and saves high-resolution publication-quality evaluation charts."""
    os.makedirs(output_dir, exist_ok=True)

    # 1. Model Comparison Chart
    plt.figure(figsize=(10, 5))
    metrics_to_plot = ['Accuracy', 'Precision', 'Recall', 'F1_Score', 'ROC_AUC']
    df_melted = df_results.melt(id_vars='Model', value_vars=metrics_to_plot, var_name='Metric', value_name='Score')
    
    ax = sns.barplot(data=df_melted, x='Model', y='Score', hue='Metric', palette='Blues_r')
    plt.title('Algorithm Performance Comparison (Test Set)', fontsize=14, fontweight='bold', pad=12)
    plt.ylabel('Score (0.0 - 1.0)', fontsize=12)
    plt.xlabel('Candidate Classifier', fontsize=12)
    plt.ylim(0.5, 1.05)
    plt.xticks(rotation=15, ha='right')
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)
    plt.tight_layout()
    comparison_path = os.path.join(output_dir, 'model_comparison.png')
    plt.savefig(comparison_path, dpi=300)
    plt.close()
    print(f"[INFO] Saved comparison plot to {comparison_path}")

    # 2. Confusion Matrix
    y_pred = model.predict(X_test_scaled)
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm, annot=True, fmt='d', cmap='Blues', cbar=False,
        xticklabels=['Healthy (0)', 'Disease (1)'],
        yticklabels=['Healthy (0)', 'Disease (1)'],
        annot_kws={'size': 14, 'fontweight': 'bold'}
    )
    plt.title(f'Confusion Matrix: {model_name}', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Predicted Label', fontsize=11, fontweight='bold')
    plt.ylabel('Actual Label', fontsize=11, fontweight='bold')
    plt.tight_layout()
    cm_path = os.path.join(output_dir, 'confusion_matrix.png')
    plt.savefig(cm_path, dpi=300)
    plt.close()
    print(f"[INFO] Saved confusion matrix to {cm_path}")

    # 3. ROC Curve
    y_prob = model.predict_proba(X_test_scaled)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    auc_score = roc_auc_score(y_test, y_prob)

    plt.figure(figsize=(7, 5))
    plt.plot(fpr, tpr, color='#2563eb', lw=2.5, label=f'{model_name} (AUC = {auc_score:.3f})')
    plt.plot([0, 1], [0, 1], color='#94a3b8', lw=1.5, linestyle='--', label='Random Chance Baseline')
    plt.xlim([-0.02, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate (1 - Specificity)', fontsize=11)
    plt.ylabel('True Positive Rate (Sensitivity / Recall)', fontsize=11)
    plt.title('Receiver Operating Characteristic (ROC) Curve', fontsize=13, fontweight='bold', pad=12)
    plt.legend(loc='lower right', frameon=True)
    plt.tight_layout()
    roc_path = os.path.join(output_dir, 'roc_curve.png')
    plt.savefig(roc_path, dpi=300)
    plt.close()
    print(f"[INFO] Saved ROC curve to {roc_path}")

    # 4. Feature Importance
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        feature_df = pd.DataFrame({
            'Feature': FEATURE_NAMES,
            'Importance': importances
        }).sort_values(by='Importance', ascending=True)

        plt.figure(figsize=(8, 6))
        plt.barh(feature_df['Feature'], feature_df['Importance'], color='#3b82f6', edgecolor='#1d4ed8')
        plt.title('Cardiovascular Risk Feature Importance Ranking', fontsize=13, fontweight='bold', pad=12)
        plt.xlabel('Relative Importance (Gini Impurity Reduction)', fontsize=11)
        plt.tight_layout()
        fi_path = os.path.join(output_dir, 'feature_importance.png')
        plt.savefig(fi_path, dpi=300)
        plt.close()
        print(f"[INFO] Saved feature importance plot to {fi_path}")


def serialize_model_and_metadata(model, scaler, best_params, metrics, model_dir='models'):
    """
    Serializes model and scaler using both Joblib and Pickle,
    and produces structured metadata JSON.
    """
    os.makedirs(model_dir, exist_ok=True)

    # 1. Joblib serialization
    joblib_model_path = os.path.join(model_dir, 'heart_disease_model.joblib')
    joblib.dump(model, joblib_model_path)
    print(f"[INFO] Serialized model with Joblib: {joblib_model_path}")

    # 2. Pickle serialization (educational requirement)
    pickle_model_path = os.path.join(model_dir, 'heart_disease_model.pkl')
    with open(pickle_model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"[INFO] Serialized model with Pickle: {pickle_model_path}")

    # 3. Model Metadata
    metadata = {
        'model_name': 'Random Forest Classifier',
        'pipeline_version': '1.1.0',
        'target_definition': '1 = Heart Disease / High Risk, 0 = Healthy / Low Risk',
        'created_at': datetime.now().isoformat(),
        'project': 'CardioPredict AI - Capstone Deployment',
        'features': FEATURE_NAMES,
        'best_hyperparameters': best_params,
        'test_metrics': metrics,
        'serialization_formats': ['joblib', 'pickle']
    }

    metadata_path = os.path.join(model_dir, 'model_metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)
    print(f"[INFO] Saved model metadata to {metadata_path}")


def execute_training_pipeline():
    """Executes the complete data-to-deployment ML training pipeline."""
    print("=" * 65)
    print("      CARDIOPREDICT AI: MACHINE LEARNING TRAINING PIPELINE")
    print("=" * 65)

    df = load_dataset()
    cleaned = validate_and_clean_data(df)
    print(f"[1/5] Loaded & cleaned dataset: {cleaned.shape[0]} patient records, {cleaned.shape[1]} columns.")

    X_train, X_test, y_train, y_test, X_train_sc, X_test_sc, scaler = prepare_train_test_data(cleaned)
    save_scaler(scaler)
    print(f"[2/5] Prepared train set ({X_train_sc.shape[0]} samples, {y_train.sum()} positive) & test set ({X_test_sc.shape[0]} samples, {y_test.sum()} positive).")

    print("[3/5] Benchmarking multiple algorithms (5-Fold Stratified Cross Validation)...")
    comparison_df, _ = train_and_compare_models(X_train_sc, y_train, X_test_sc, y_test)
    print("\n--- Model Benchmark Table ---")
    print(comparison_df.to_string(index=False))

    print("\n[4/5] Hyperparameter tuning optimal model (Random Forest)...")
    tuned_model, best_params = tune_best_model(X_train_sc, y_train)

    # Evaluate tuned model on holdout test set
    y_pred = tuned_model.predict(X_test_sc)
    y_prob = tuned_model.predict_proba(X_test_sc)[:, 1]

    metrics = {
        'accuracy': round(float(accuracy_score(y_test, y_pred)), 4),
        'precision': round(float(precision_score(y_test, y_pred)), 4),
        'recall': round(float(recall_score(y_test, y_pred)), 4),
        'f1_score': round(float(f1_score(y_test, y_pred)), 4),
        'roc_auc': round(float(roc_auc_score(y_test, y_prob)), 4)
    }

    print("\n--- Final Test Set Evaluation ---")
    for k, v in metrics.items():
        print(f"  {k.upper()}: {v * 100:.2f}%")
    print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=['Healthy / Low Risk', 'Heart Disease / High Risk']))

    print("[5/5] Generating diagnostic charts & serializing model artifacts...")
    generate_evaluation_visualizations(tuned_model, 'Random Forest (Tuned)', comparison_df, X_test_sc, y_test)
    serialize_model_and_metadata(tuned_model, scaler, best_params, metrics)

    # Copy plots to app/static/plots
    import shutil
    os.makedirs('app/static/plots', exist_ok=True)
    for f in os.listdir('reports/plots'):
        if f.endswith('.png'):
            shutil.copy(os.path.join('reports/plots', f), os.path.join('app/static/plots', f))

    print("\n" + "=" * 65)
    print("  TRAINING & SERIALIZATION COMPLETED SUCCESSFULLY!")
    print("=" * 65)
    return tuned_model, scaler, metrics, comparison_df


if __name__ == '__main__':
    execute_training_pipeline()
