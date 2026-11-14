"""
Script to generate the comprehensive Word Document (.docx) Capstone Project Report
Author: Aafiya Kulsum
Internship: AI Pioneers Internship (Yuva Intern) - Week 4 AI Capstone
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def set_cell_background(cell, hex_color):
    """Sets background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tc_pr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets padding for a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tc_pr.append(tcMar)


def build_docx_report(output_path='reports/Aafiya_Kulsum_Week4_AI_Capstone_Report.docx'):
    doc = docx.Document()

    # Set page margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Style colors
    COLOR_PRIMARY = RGBColor(30, 58, 138)    # Deep Navy #1E3A8A
    COLOR_SECONDARY = RGBColor(14, 116, 144) # Teal/Cyan #0E7490
    COLOR_TEXT = RGBColor(31, 41, 55)        # Slate Dark #1F2937
    COLOR_MUTED = RGBColor(100, 116, 139)    # Muted Grey #64748B

    # Document Header / Cover Info
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(20)
    title_p.paragraph_format.space_after = Pt(6)
    title_run = title_p.add_run("CardioPredict AI: End-to-End Heart Disease Risk Prediction & Clinical Decision Support System")
    title_run.font.name = 'Arial'
    title_run.font.size = Pt(24)
    title_run.font.bold = True
    title_run.font.color.rgb = COLOR_PRIMARY

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(18)
    sub_run = sub_p.add_run("AI Pioneers Internship — Week 4 Final AI Capstone Project Report")
    sub_run.font.name = 'Arial'
    sub_run.font.size = Pt(14)
    sub_run.font.italic = True
    sub_run.font.color.rgb = COLOR_SECONDARY

    # Metadata Table
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Candidate Name:", "Aafiya Kulsum"),
        ("Internship Program:", "AI Pioneers Internship (Yuva Intern)"),
        ("Milestone / Task:", "Week 4 Task: AI Project Deployment & Capstone"),
        ("Deliverable Type:", "End-to-End Machine Learning Deployment & Technical Documentation"),
        ("Date of Submission:", "November 2026")
    ]
    for i, (k, v) in enumerate(meta_data):
        row = meta_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(k)
        r0.font.bold = True
        r0.font.size = Pt(10.5)
        r0.font.color.rgb = COLOR_PRIMARY
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(v)
        r1.font.size = Pt(10.5)
        set_cell_background(c0, "F1F5F9")
        set_cell_background(c1, "F8FAFC")
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    doc.add_page_break()

    # Helper function for Section Headings
    def add_heading_1(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(16)
        h.paragraph_format.space_after = Pt(6)
        h.paragraph_format.keep_with_next = True
        run = h.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        return h

    def add_heading_2(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
        run = h.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = COLOR_SECONDARY
        return h

    def add_body(text, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(10.5)
        run.font.color.rgb = COLOR_TEXT
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r0 = p.add_run(bold_prefix)
        r0.font.name = 'Arial'
        r0.font.size = Pt(10.5)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_PRIMARY
        r1 = p.add_run(text)
        r1.font.name = 'Arial'
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = COLOR_TEXT
        return p

    # 1. Executive Summary
    add_heading_1("1. Executive Summary")
    add_body(
        "Cardiovascular diseases (CVDs) remain the leading cause of global mortality, claiming an estimated 17.9 million "
        "lives each year according to the World Health Organization. Early identification of clinical risk factors provides "
        "a critical window for medical intervention, lifestyle modification, and morbidity reduction. This Capstone Project, "
        "titled 'CardioPredict AI', delivers an end-to-end Machine Learning pipeline and deployment ecosystem engineered to predict "
        "coronary heart disease risk from patient clinical biomarkers."
    )
    add_body(
        "The project encompasses rigorous exploratory data analysis, data pre-processing, feature scaling via StandardScaler, "
        "stratified model comparison across 5 candidate algorithms (Logistic Regression, Random Forest, Support Vector Machine, "
        "Gradient Boosting, and K-Nearest Neighbors), hyperparameter tuning via GridSearchCV, model serialization using both "
        "Joblib and Pickle, and production deployment through a modern Flask web application and RESTful microservice API."
    )
    add_body(
        "The optimal model—a tuned Random Forest Classifier—achieved an exceptional 93.94% clinical recall and a 90.80% ROC-AUC score "
        "on the holdout test set, ensuring high sensitivity in detecting ischemic heart disease. The complete system includes an "
        "interactive graphical user interface (UI), real-time risk gauge, personalized lifestyle recommendations, automated unit "
        "and integration test suites, and OpenAPI/JSON prediction endpoints for electronic health record (EHR) integration."
    )

    # 2. Objectives & Project Scope
    add_heading_1("2. Objectives & Deliverables Breakdown")
    add_body(
        "The project was designed and implemented to satisfy the core learning outcomes of the AI Pioneers Internship Capstone:"
    )
    add_bullet("Objective 1: End-to-End Pipeline — ", "Execute full lifecycle ML development comprising data ingestion, missing value imputation, duplicate removal, feature standardization, stratified train/test partitioning, and model training.")
    add_bullet("Objective 2: Model Serialization — ", "Implement industry-standard model persistence using Joblib and Pickle, comparing computational speed, byte footprint, security safeguards, and versioned metadata storage.")
    add_bullet("Objective 3: RESTful Microservice & UI Deployment — ", "Develop and host a robust Flask web server featuring dual operational modes: an accessible clinician/patient web portal and an enterprise JSON REST API endpoint.")
    add_bullet("Objective 4: Quality Assurance & Testing — ", "Design an automated test harness verifying data schema validation, model inference stability, probability calibration, and API HTTP error handling.")
    add_bullet("Objective 5: Capstone Documentation & Presentation — ", "Compile comprehensive technical documentation and professional presentation slides synthesizing architecture, benchmark results, and clinical deployment strategy.")

    # 3. Dataset Description & Clinical Biomarkers
    add_heading_1("3. Dataset Description & Feature Dictionary")
    add_body(
        "The system utilizes the gold-standard Cleveland Heart Disease Dataset sourced from the UCI Machine Learning Repository. "
        "The dataset contains 303 patient records with 13 physiological and clinical input features and 1 binary diagnostic target."
    )

    # Feature Dictionary Table
    feat_table = doc.add_table(rows=14, cols=4)
    feat_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Feature", "Clinical Description", "Type / Range", "Normal Reference"]
    hdr_row = feat_table.rows[0]
    for i, h in enumerate(headers):
        cell = hdr_row.cells[i]
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, 80, 80, 100, 100)

    feature_data = [
        ("age", "Patient Age in Years", "Integer [29 - 77]", "Adult cohort"),
        ("sex", "Biological Sex", "Binary (1=Male, 0=Female)", "Demographic"),
        ("cp", "Chest Pain Type", "Categorical [0 - 3]", "0: Typical, 1: Atypical, 2: Non-anginal, 3: Asymptomatic"),
        ("trestbps", "Resting Blood Pressure", "Continuous [94 - 200 mm Hg]", "< 120 mm Hg (AHA standard)"),
        ("chol", "Serum Cholesterol", "Continuous [126 - 564 mg/dl]", "< 200 mg/dl (Desirable)"),
        ("fbs", "Fasting Blood Sugar > 120 mg/dl", "Binary (1=True, 0=False)", "0 (Normal glucose metabolism)"),
        ("restecg", "Resting Electrocardiogram", "Categorical [0, 1, 2]", "0: Normal, 1: ST-T wave anomaly, 2: LVH"),
        ("thalach", "Maximum Heart Rate Achieved", "Continuous [71 - 202 bpm]", "Est. Max = 220 - Age"),
        ("exang", "Exercise Induced Angina", "Binary (1=Yes, 0=No)", "0 (No angina during stress test)"),
        ("oldpeak", "ST Depression Induced by Exercise", "Continuous [0.0 - 6.2 mm]", "< 1.0 mm (Relative to rest)"),
        ("slope", "Slope of Peak Exercise ST", "Categorical [0, 1, 2]", "0: Upsloping, 1: Flat, 2: Downsloping"),
        ("ca", "Number of Major Vessels Colored", "Integer [0 - 3 vessels]", "0 (No coronary vessel occlusion)"),
        ("thal", "Thallium Stress Scintigraphy", "Categorical [1, 2, 3]", "1: Normal, 2: Fixed defect, 3: Reversible")
    ]

    for idx, row_data in enumerate(feature_data):
        row = feat_table.rows[idx + 1]
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.font.bold = True
            bg = "F8FAFC" if idx % 2 == 0 else "FFFFFF"
            set_cell_background(cell, bg)
            set_cell_margins(cell, 50, 50, 80, 80)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 4. Exploratory Data Analysis & Preprocessing
    add_heading_1("4. Exploratory Data Analysis & Preprocessing Pipeline")
    add_body(
        "A reliable machine learning system depends fundamentally on disciplined data preprocessing. "
        "The CardioPredict AI data engineering module (data_preprocessing.py) performs the following systematic procedures:"
    )
    add_bullet("Integrity Verification & Deduplication: ", "The dataset was checked for null values, inconsistent types, and duplicate rows. One duplicate record was identified and removed, yielding 302 unique patient profiles.")
    add_bullet("Stratified Data Partitioning: ", "To prevent sampling bias and maintain the real-world disease incidence ratio (54.5% positive, 45.5% negative), a Stratified 80/20 train/test split was enforced with a fixed seed (random_state=42). This produced 241 training records and 61 unseen holdout test samples.")
    add_bullet("Feature Standardization (StandardScaler): ", "Continuous clinical variables (cholesterol, blood pressure, heart rate, age, oldpeak) span significantly different magnitudes. To ensure gradient-based and distance-based algorithms operate without scale bias, a StandardScaler was fitted strictly on X_train and applied to transform both X_train and X_test, avoiding data leakage.")
    add_bullet("Scaler Serialization: ", "The fitted StandardScaler instance was serialized into models/scaler.joblib, ensuring identical mathematical scaling parameters (mean and standard deviation vectors) are applied during live inference in production.")

    # 5. Model Training & Comparative Benchmarking
    add_heading_1("5. Model Training & Algorithm Benchmarking")
    add_body(
        "To establish the optimal architectural backbone, five distinct classification paradigms were trained and evaluated "
        "under 5-Fold Stratified Cross-Validation on the training partition and validated against the unseen test dataset:"
    )

    # Benchmark Results Table
    bench_table = doc.add_table(rows=6, cols=6)
    bench_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    b_headers = ["Algorithm", "CV F1 (Mean ± Std)", "Test Accuracy", "Test Precision", "Test Recall", "Test ROC-AUC"]
    for i, h in enumerate(b_headers):
        cell = bench_table.rows[0].cells[i]
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9.0)
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, 70, 70, 80, 80)

    bench_data = [
        ("Support Vector Machine (SVC)", "0.8252 ± 0.045", "83.61%", "79.49%", "93.94%", "0.8810"),
        ("Gradient Boosting Classifier", "0.7841 ± 0.074", "81.97%", "80.56%", "87.88%", "0.8690"),
        ("K-Nearest Neighbors (KNN)", "0.8188 ± 0.039", "80.33%", "76.92%", "90.91%", "0.8674"),
        ("Logistic Regression", "0.8379 ± 0.051", "78.69%", "76.32%", "87.88%", "0.8647"),
        ("Random Forest (Tuned Ensemble)", "0.8673 ± 0.032", "81.97%", "77.50%", "93.94%", "0.9080")
    ]

    for idx, row_data in enumerate(bench_data):
        row = bench_table.rows[idx + 1]
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if idx == 4: # Tuned model highlight
                r.font.bold = True
                set_cell_background(cell, "DCFCE7") # Light green highlight
            else:
                bg = "F8FAFC" if idx % 2 == 0 else "FFFFFF"
                set_cell_background(cell, bg)
            set_cell_margins(cell, 50, 50, 80, 80)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Embed Model Comparison Chart
    comp_plot = 'reports/plots/model_comparison.png'
    if os.path.exists(comp_plot):
        add_heading_2("Figure 1: Multi-Model Metric Benchmark Comparison")
        doc.add_picture(comp_plot, width=Inches(6.0))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap = doc.add_paragraph()
        cap.paragraph_format.space_after = Pt(10)
        c_run = cap.add_run("Figure 1: Performance metrics comparison across all 5 benchmarked classifiers on the holdout test set.")
        c_run.font.size = Pt(8.5)
        c_run.font.italic = True
        c_run.font.color.rgb = COLOR_MUTED
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 6. Hyperparameter Tuning & Optimal Model Selection
    add_heading_1("6. Hyperparameter Tuning & Diagnostic Evaluation")
    add_body(
        "In healthcare diagnostics, model selection cannot be dictated solely by generic accuracy. A False Negative (classifying "
        "a heart disease patient as healthy) carries catastrophic clinical consequences, whereas a False Positive prompts benign "
        "confirmatory screening. Therefore, Recall (Sensitivity) and ROC-AUC are paramount."
    )
    add_body(
        "Random Forest was chosen as the primary deployment engine due to its superior ensemble resilience, low variance, "
        "and clear probability calibration. Using 5-Fold Stratified GridSearchCV across n_estimators, max_depth, min_samples_split, "
        "and min_samples_leaf, the optimal hyperparameters were determined:"
    )
    add_bullet("Number of Estimators (n_estimators): ", "100 decision trees")
    add_bullet("Minimum Samples Split (min_samples_split): ", "5 samples required to split an internal node")
    add_bullet("Minimum Samples Leaf (min_samples_leaf): ", "2 samples required per leaf node (regularization against overfitting)")
    add_bullet("Class Weight: ", "None (balanced natural prevalence)")

    # Embed Confusion Matrix and ROC Curve side by side or sequentially
    cm_plot = 'reports/plots/confusion_matrix.png'
    roc_plot = 'reports/plots/roc_curve.png'
    fi_plot = 'reports/plots/feature_importance.png'

    if os.path.exists(cm_plot):
        add_heading_2("Figure 2: Confusion Matrix of the Tuned Random Forest Model")
        doc.add_picture(cm_plot, width=Inches(4.5))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap = doc.add_paragraph()
        cap.paragraph_format.space_after = Pt(10)
        c_run = cap.add_run("Figure 2: Holdout confusion matrix demonstrating 31/33 True Positives (93.94% clinical recall).")
        c_run.font.size = Pt(8.5)
        c_run.font.italic = True
        c_run.font.color.rgb = COLOR_MUTED
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER

    if os.path.exists(roc_plot):
        add_heading_2("Figure 3: Receiver Operating Characteristic (ROC) Curve")
        doc.add_picture(roc_plot, width=Inches(5.0))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap = doc.add_paragraph()
        cap.paragraph_format.space_after = Pt(10)
        c_run = cap.add_run("Figure 3: Area Under Curve (ROC-AUC = 0.908), confirming robust discrimination across decision thresholds.")
        c_run.font.size = Pt(8.5)
        c_run.font.italic = True
        c_run.font.color.rgb = COLOR_MUTED
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER

    if os.path.exists(fi_plot):
        add_heading_2("Figure 4: Clinical Feature Importance Ranking")
        doc.add_picture(fi_plot, width=Inches(5.5))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap = doc.add_paragraph()
        cap.paragraph_format.space_after = Pt(10)
        c_run = cap.add_run("Figure 4: Gini impurity reduction ranking highlighting thal, ca, thalach, and oldpeak as top predictive biomarkers.")
        c_run.font.size = Pt(8.5)
        c_run.font.italic = True
        c_run.font.color.rgb = COLOR_MUTED
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 7. Model Serialization Analysis (Joblib vs Pickle)
    add_heading_1("7. Model Serialization Analysis: Joblib vs. Pickle")
    add_body(
        "A core objective of this project is mastering model serialization to bridge offline training and live production serving. "
        "Both Joblib and Python's native Pickle library were implemented and evaluated:"
    )

    ser_table = doc.add_table(rows=5, cols=3)
    ser_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_headers = ["Evaluation Dimension", "Joblib (models/heart_disease_model.joblib)", "Pickle (models/heart_disease_model.pkl)"]
    for i, h in enumerate(s_headers):
        cell = ser_table.rows[0].cells[i]
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9.0)
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, 70, 70, 80, 80)

    ser_data = [
        ("Numpy Array Optimization", "Highly optimized for large multi-dimensional matrices with memory mapping.", "Standard serialization; lacks dedicated memory chunking."),
        ("Disk Storage Size", "239 KB (compact single-file serialization)", "241 KB"),
        ("Loading Latency", "~ 3.2 ms average cold load time", "~ 4.1 ms average load time"),
        ("Production Recommendation", "Industry standard for Scikit-Learn pipelines & production serving.", "Standard Python persistence; optimal for pure native types.")
    ]

    for idx, row_data in enumerate(ser_data):
        row = ser_table.rows[idx + 1]
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.font.bold = True
            bg = "F8FAFC" if idx % 2 == 0 else "FFFFFF"
            set_cell_background(cell, bg)
            set_cell_margins(cell, 50, 50, 80, 80)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 8. Flask Web Application & REST API Deployment
    add_heading_1("8. Web Application & REST API Microservice Architecture")
    add_body(
        "The deployment module (app/app.py) was built using Flask, providing dual access channels for end-users and software integrations:"
    )
    add_bullet("1. Interactive Web Interface (/ and /predict): ", "A modern, responsive user portal built with Bootstrap 5 and custom CSS. Allows clinicians to input patient biomarkers manually or load curated 'Healthy' and 'High-Risk' test profiles with a single click. Upon submission, it generates an exportable, printable clinical evaluation report.")
    add_bullet("2. RESTful Prediction API (/api/predict): ", "A stateless JSON microservice accepting POST requests with 13 input features, executing real-time data scaling, returning class predictions (0/1), probability percentages, risk categories ('Low', 'Moderate', 'High Risk'), and personalized medical guidance.")
    add_bullet("3. Model Specifications Endpoint (/api/models/info): ", "Provides programmatic inspection of model version, training timestamp, feature list, and test benchmark metrics.")
    add_bullet("4. Microservice Health Probe (/health): ", "Supports containerized orchestration (Docker/Kubernetes) by reporting server readiness and artifact loading state.")

    # 9. Automated Testing & Verification
    add_heading_1("9. Automated Testing & Quality Assurance")
    add_body(
        "An enterprise-ready project requires rigorous verification. The CardioPredict AI test suite (test_suite.py) executes 11 unit "
        "and integration test cases covering all architectural layers:"
    )
    add_bullet("Preprocessing Tests (tests/test_preprocessing.py): ", "Verifies dataset presence, column schemas, null handling, duplicate removal, and mathematical correctness of StandardScaler.")
    add_bullet("Model Inference Tests (tests/test_model.py): ", "Verifies Joblib and Pickle loading parity, guaranteeing identical floating-point prediction probabilities and ensuring bounds [0.0, 1.0].")
    add_bullet("API Integration Tests (tests/test_api.py): ", "Validates HTTP 200 responses on valid payloads, schema validation and HTTP 400 error codes on incomplete payloads, and correct HTML rendering.")

    # 10. Conclusion & Future Roadmap
    add_heading_1("10. Conclusion & Future Roadmap")
    add_body(
        "CardioPredict AI successfully demonstrates the complete lifecycle of an applied Machine Learning solution—from raw tabular "
        "data ingestion to production-grade model serving and clinical decision support. By attaining a 93.94% recall and 90.80% ROC-AUC, "
        "the system establishes strong predictive power while prioritizing patient safety through high sensitivity."
    )
    add_body(
        "Key future enhancements include:"
    )
    add_bullet("1. Containerization & Cloud Deployment: ", "Packaging the Flask application into a Docker container for deployment to AWS ECS, Google Cloud Run, or Azure App Service.")
    add_bullet("2. Explainable AI (XAI): ", "Integrating SHAP (SHapley Additive exPlanations) and LIME to generate patient-specific visual force plots explaining why a specific prediction was rendered.")
    add_bullet("3. Continuous Learning & Data Drift Detection: ", "Deploying Prometheus and Evidently AI to monitor model performance and feature drift across shifting demographic populations.")

    # Save document
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"[SUCCESS] Saved Word Document report to: {output_path}")


if __name__ == '__main__':
    build_docx_report()
