"""
CardioPredict AI: Flask Application & RESTful Prediction Microservice
Clinical Decision Support System for Heart Disease Risk Stratification.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='templates', static_folder='static')

# File paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'heart_disease_model.joblib')
SCALER_PATH = os.path.join(BASE_DIR, 'models', 'scaler.joblib')
METADATA_PATH = os.path.join(BASE_DIR, 'models', 'model_metadata.json')

FEATURE_NAMES = [
    'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
    'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
]

# Lazy-loaded model and scaler
model = None
scaler = None
metadata = {}


def load_artifacts():
    """Loads serialized ML model, scaler, and metadata."""
    global model, scaler, metadata
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    if os.path.exists(SCALER_PATH):
        scaler = joblib.load(SCALER_PATH)
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, 'r') as f:
            metadata = json.load(f)


load_artifacts()


def generate_clinical_recommendations(prob: float, inputs: dict):
    """Generates personalized clinical and lifestyle guidance based on patient parameters."""
    recs = []

    if prob >= 65.0:
        recs.append({
            'title': 'Cardiology Specialist Consultation',
            'description': 'Elevated coronary risk profile detected. Comprehensive clinical workup including 12-lead ECG and echocardiogram is strongly advised.'
        })
    elif prob >= 40.0:
        recs.append({
            'title': 'Preventive Cardiometabolic Review',
            'description': 'Moderate cardiac risk profile observed. Routine cardiovascular screening and risk stratification advised within 30-60 days.'
        })
    else:
        recs.append({
            'title': 'Optimal Cardiac Baseline',
            'description': 'Evaluated indicators are healthy and within normal boundaries. Continue annual wellness evaluations and cardiovascular conditioning.'
        })

    # Biomarker-specific guidance
    if inputs.get('trestbps', 0) >= 130:
        recs.append({
            'title': 'Blood Pressure Optimization',
            'description': f'Resting systolic BP of {inputs.get("trestbps")} mm Hg is elevated. Adopt DASH dietary plan and monitor daily BP.'
        })

    if inputs.get('chol', 0) >= 200:
        recs.append({
            'title': 'Lipid Management Protocol',
            'description': f'Serum cholesterol of {inputs.get("chol")} mg/dl exceeds recommended limits (<200 mg/dl). Reduce dietary saturated fats.'
        })

    if inputs.get('exang', 0) == 1:
        recs.append({
            'title': 'Exertion Angina Caution',
            'description': 'Exercise-induced chest tightness reported. Avoid sudden high-intensity exertion prior to physician treadmill clearance.'
        })

    if inputs.get('fbs', 0) == 1:
        recs.append({
            'title': 'Glycemic Screening',
            'description': 'Fasting blood glucose > 120 mg/dl indicated. Perform HbA1c test to evaluate diabetic comorbidities.'
        })

    if inputs.get('ca', 0) > 0:
        recs.append({
            'title': 'Coronary Vessel Monitoring',
            'description': f'{int(inputs.get("ca"))} major vessel(s) showed fluoroscopic opacity. Follow up with CT coronary angiogram.'
        })

    return recs


@app.route('/')
def home():
    """Renders the interactive web assessment dashboard."""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict_web():
    """Handles HTML form submissions and renders detailed clinical report."""
    load_artifacts()
    try:
        inputs = {}
        for feat in FEATURE_NAMES:
            val = request.form.get(feat)
            if val is None:
                return f"Missing form field: {feat}", 400
            inputs[feat] = float(val)

        df_input = pd.DataFrame([inputs])[FEATURE_NAMES]
        X_scaled = scaler.transform(df_input)

        prediction = int(model.predict(X_scaled)[0])
        prob = float(model.predict_proba(X_scaled)[0, 1]) * 100.0

        if prob >= 65.0:
            risk_level = "High Risk"
            alert_class = "alert-danger"
            badge_class = "bg-danger text-white"
            progress_class = "bg-danger"
            text_color = "text-danger"
            icon_class = "fa-solid fa-triangle-exclamation"
            diag_title = "High Probability of Coronary Heart Disease"
            diag_summary = "Patient clinical indicators strongly match positive ischemic cardiovascular disease profiles. Immediate cardiology follow-up is recommended."
        elif prob >= 40.0:
            risk_level = "Moderate Risk"
            alert_class = "alert-warning"
            badge_class = "bg-warning text-dark"
            progress_class = "bg-warning"
            text_color = "text-warning-emphasis"
            icon_class = "fa-solid fa-circle-exclamation"
            diag_title = "Moderate Cardiovascular Risk Profile"
            diag_summary = "Borderline physiological indicators detected. Early cardiometabolic intervention and lifestyle modification are recommended."
        else:
            risk_level = "Low Risk"
            alert_class = "alert-success"
            badge_class = "bg-success text-white"
            progress_class = "bg-success"
            text_color = "text-success"
            icon_class = "fa-solid fa-circle-check"
            diag_title = "Low Heart Disease Risk Profile"
            diag_summary = "Evaluated physiological biomarkers fall comfortably within favorable, healthy cardiovascular reference boundaries."

        cp_labels = {
            0: "0: Typical Angina (Severe)",
            1: "1: Atypical Angina",
            2: "2: Non-Anginal Chest Pain",
            3: "3: Asymptomatic"
        }
        cp_text = cp_labels.get(int(inputs['cp']), f"Type {int(inputs['cp'])}")

        recommendations = generate_clinical_recommendations(prob, inputs)

        return render_template(
            'result.html',
            inputs=inputs,
            prediction=prediction,
            probability=round(prob, 2),
            risk_level=risk_level,
            alert_class=alert_class,
            badge_class=badge_class,
            progress_class=progress_class,
            text_color=text_color,
            icon_class=icon_class,
            diagnosis_title=diag_title,
            diagnosis_summary=diag_summary,
            cp_text=cp_text,
            recommendations=recommendations,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    except Exception as e:
        return f"Error during prediction: {str(e)}", 500


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """RESTful API endpoint for heart disease risk predictions."""
    load_artifacts()
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'Invalid request: Request body must be valid JSON application/json.'
        }), 400

    missing_fields = [f for f in FEATURE_NAMES if f not in data]
    if missing_fields:
        return jsonify({
            'status': 'error',
            'message': f'Missing required biomarker fields: {missing_fields}',
            'required_fields': FEATURE_NAMES
        }), 400

    try:
        row = {f: float(data[f]) for f in FEATURE_NAMES}
        df_input = pd.DataFrame([row])[FEATURE_NAMES]
        X_scaled = scaler.transform(df_input)

        prediction = int(model.predict(X_scaled)[0])
        prob = float(model.predict_proba(X_scaled)[0, 1]) * 100.0

        if prob >= 65.0:
            risk_level = "High Risk"
            diag = "Heart Disease Indicated"
        elif prob >= 40.0:
            risk_level = "Moderate Risk"
            diag = "Moderate Cardiovascular Risk"
        else:
            risk_level = "Low Risk"
            diag = "Healthy / Low Risk Profile"

        recommendations = generate_clinical_recommendations(prob, row)

        return jsonify({
            'status': 'success',
            'prediction': prediction,
            'diagnosis': diag,
            'probability': round(prob, 2),
            'risk_level': risk_level,
            'timestamp': datetime.now().isoformat(),
            'recommendations': recommendations
        }), 200

    except ValueError as ve:
        return jsonify({'status': 'error', 'message': f'Invalid value format: {str(ve)}'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Inference engine error: {str(e)}'}), 500


@app.route('/api/models/info', methods=['GET'])
def api_model_info():
    """Returns model architecture, features, and test performance metrics."""
    load_artifacts()
    return jsonify({
        'status': 'success',
        'metadata': metadata
    }), 200


@app.route('/health', methods=['GET'])
def health_check():
    """Health check microservice probe."""
    return jsonify({
        'status': 'healthy',
        'service': 'CardioPredict AI Prediction Engine',
        'model_loaded': model is not None,
        'scaler_loaded': scaler is not None
    }), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
