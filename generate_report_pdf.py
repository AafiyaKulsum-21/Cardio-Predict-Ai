"""
Script to generate the comprehensive, publication-grade PDF Capstone Project Report
Author: Aafiya Kulsum
Internship: AI Pioneers Internship (Yuva Intern) - Week 4 AI Capstone
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and print 'Page X of Y' and running headers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Running header on pages 2+
        if self._pageNumber > 1:
            self.drawString(54, 752, "CardioPredict AI — End-to-End Clinical Risk Prediction System")
            self.drawRightString(558, 752, "AI Pioneers Capstone Report")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 746, 558, 746)

        # Running footer on all pages
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)

        self.drawString(54, 34, "Author: Aafiya Kulsum | AI Pioneers Internship (Yuva Intern)")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 34, page_str)
        self.restoreState()


def build_pdf_report(output_path='reports/Aafiya_Kulsum_Week4_AI_Capstone_Report.pdf'):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 54 pt margins = 0.75 inch
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor("#1E3A8A")     # Deep Navy
    SECONDARY = colors.HexColor("#0E7490")   # Teal
    ACCENT = colors.HexColor("#2563EB")      # Azure
    DARK_TEXT = colors.HexColor("#1F2937")   # Slate Dark
    MUTED = colors.HexColor("#64748B")       # Slate Muted
    LIGHT_BG = colors.HexColor("#F8FAFC")
    BORDER_COLOR = colors.HexColor("#E2E8F0")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=PRIMARY,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT,
        leftIndent=15,
        spaceAfter=3
    )

    caption_style = ParagraphStyle(
        'CaptionCustom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=MUTED,
        alignment=1, # Centered
        spaceBefore=4,
        spaceAfter=10
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=DARK_TEXT
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.white
    )

    story = []

    # ----------------- COVER / HEADER BANNER -----------------
    story.append(Paragraph("CardioPredict AI: End-to-End Heart Disease Risk Prediction & Clinical Decision Support System", title_style))
    story.append(Paragraph("AI Pioneers Internship — Week 4 Final AI Capstone Project Report", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceBefore=0, spaceAfter=10))

    # Metadata Table
    meta_data = [
        [Paragraph("<b>Candidate Name:</b>", table_cell_style), Paragraph("Aafiya Kulsum (aafiyak.2006@gmail.com)", table_cell_style)],
        [Paragraph("<b>Internship Program:</b>", table_cell_style), Paragraph("AI Pioneers Internship (Yuva Intern)", table_cell_style)],
        [Paragraph("<b>Milestone / Task:</b>", table_cell_style), Paragraph("Week 4 Task: AI Project Deployment & Capstone", table_cell_style)],
        [Paragraph("<b>Deliverables Covered:</b>", table_cell_style), Paragraph("Data Preprocessing, ML Training & Comparison, Joblib/Pickle Serialization, Flask REST API & Web UI, Automated Test Suite, Word/PDF Report & Presentation", table_cell_style)],
        [Paragraph("<b>Submission Date:</b>", table_cell_style), Paragraph("November 2026", table_cell_style)]
    ]
    meta_table = Table(meta_data, colWidths=[130, 374])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    # ----------------- 1. EXECUTIVE SUMMARY -----------------
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "Cardiovascular diseases (CVDs) remain the leading cause of global mortality, claiming an estimated 17.9 million "
        "lives annually according to the World Health Organization. Early clinical identification of coronary heart disease risk "
        "provides an essential window for medical triage and lifestyle intervention. This Capstone Project, <b>'CardioPredict AI'</b>, "
        "implements an end-to-end Machine Learning solution that analyzes non-invasive patient clinical biomarkers to compute disease "
        "probabilities, output categorical risk strata, and furnish targeted clinical guidance.",
        body_style
    ))
    story.append(Paragraph(
        "The project demonstrates rigorous data hygiene, feature scaling via <code>StandardScaler</code>, 5-Fold Stratified Cross-Validation, "
        "hyperparameter optimization, dual model serialization via <b>Joblib</b> and <b>Pickle</b>, and production deployment through a "
        "high-performance <b>Flask</b> web application and RESTful microservice. The optimal classifier—a tuned Random Forest—achieved "
        "a <b>93.94% clinical recall (sensitivity)</b> and a <b>90.80% ROC-AUC score</b> on holdout test data, successfully prioritizing "
        "patient safety by minimizing false-negative diagnostic errors.",
        body_style
    ))

    # ----------------- 2. OBJECTIVES & DELIVERABLES -----------------
    story.append(Paragraph("2. Objectives & Deliverables Breakdown", h1_style))
    story.append(Paragraph("The project was executed to satisfy all requirements specified in the Week 4 Internship Capstone syllabus:", body_style))
    story.append(Paragraph("• <b>Objective 1: End-to-End ML Pipeline:</b> Ingestion, schema validation, deduplication, StandardScaler transformation, 80/20 stratified partitioning, and multi-algorithm training.", bullet_style))
    story.append(Paragraph("• <b>Objective 2: Model Serialization:</b> Comparative implementation of Joblib and Pickle serialization, verifying exact inference parity and exporting versioned JSON metadata.", bullet_style))
    story.append(Paragraph("• <b>Objective 3: RESTful Microservice & UI Deployment:</b> Dual serving modes with an accessible browser UI (featuring one-click test sample loading) and an OpenAPI JSON endpoint (<code>/api/predict</code>).", bullet_style))
    story.append(Paragraph("• <b>Objective 4: Quality Assurance & Testing:</b> 11 automated unit and integration tests verifying data integrity, model consistency, and HTTP status codes with 100% pass rate.", bullet_style))
    story.append(Paragraph("• <b>Objective 5: Capstone Documentation:</b> Comprehensive academic and engineering report in both Word (.docx) and PDF formats, accompanied by a 16:9 widescreen presentation deck (.pptx).", bullet_style))

    # ----------------- 3. DATASET DESCRIPTION -----------------
    story.append(Paragraph("3. Dataset Description & Clinical Feature Dictionary", h1_style))
    story.append(Paragraph(
        "The system utilizes the gold-standard Cleveland Heart Disease dataset from the UCI Machine Learning Repository, "
        "comprising 303 patient records across 13 physiological features and 1 diagnostic target:",
        body_style
    ))

    feat_rows = [
        [Paragraph("Feature", table_header_style), Paragraph("Clinical Description", table_header_style), Paragraph("Type / Range", table_header_style), Paragraph("Standard Clinical Reference", table_header_style)],
        [Paragraph("<b>age</b>", table_cell_style), Paragraph("Patient age in years", table_cell_style), Paragraph("Integer [29 – 77]", table_cell_style), Paragraph("Adult demographic cohort", table_cell_style)],
        [Paragraph("<b>sex</b>", table_cell_style), Paragraph("Biological sex", table_cell_style), Paragraph("Binary (1=Male, 0=Female)", table_cell_style), Paragraph("Baseline demographic", table_cell_style)],
        [Paragraph("<b>cp</b>", table_cell_style), Paragraph("Chest pain symptom type", table_cell_style), Paragraph("Categorical [0 – 3]", table_cell_style), Paragraph("0: Typical, 1: Atypical, 2: Non-anginal, 3: Asymptomatic", table_cell_style)],
        [Paragraph("<b>trestbps</b>", table_cell_style), Paragraph("Resting blood pressure", table_cell_style), Paragraph("Continuous [94 – 200 mm Hg]", table_cell_style), Paragraph("&lt; 120 mm Hg (AHA standard)", table_cell_style)],
        [Paragraph("<b>chol</b>", table_cell_style), Paragraph("Serum cholesterol", table_cell_style), Paragraph("Continuous [126 – 564 mg/dl]", table_cell_style), Paragraph("&lt; 200 mg/dl (Desirable)", table_cell_style)],
        [Paragraph("<b>fbs</b>", table_cell_style), Paragraph("Fasting blood sugar &gt; 120 mg/dl", table_cell_style), Paragraph("Binary (1=True, 0=False)", table_cell_style), Paragraph("0 (Normal fasting glucose)", table_cell_style)],
        [Paragraph("<b>restecg</b>", table_cell_style), Paragraph("Resting electrocardiogram", table_cell_style), Paragraph("Categorical [0, 1, 2]", table_cell_style), Paragraph("0: Normal, 1: ST-T wave anomaly, 2: LVH", table_cell_style)],
        [Paragraph("<b>thalach</b>", table_cell_style), Paragraph("Maximum achieved heart rate", table_cell_style), Paragraph("Continuous [71 – 202 bpm]", table_cell_style), Paragraph("Est. Max = 220 – Age", table_cell_style)],
        [Paragraph("<b>exang</b>", table_cell_style), Paragraph("Exercise induced angina", table_cell_style), Paragraph("Binary (1=Yes, 0=No)", table_cell_style), Paragraph("0 (No angina during stress test)", table_cell_style)],
        [Paragraph("<b>oldpeak</b>", table_cell_style), Paragraph("ST depression relative to rest", table_cell_style), Paragraph("Continuous [0.0 – 6.2 mm]", table_cell_style), Paragraph("&lt; 1.0 mm (Normal)", table_cell_style)],
        [Paragraph("<b>slope</b>", table_cell_style), Paragraph("Slope of peak exercise ST segment", table_cell_style), Paragraph("Categorical [0, 1, 2]", table_cell_style), Paragraph("0: Upsloping, 1: Flat, 2: Downsloping", table_cell_style)],
        [Paragraph("<b>ca</b>", table_cell_style), Paragraph("Major vessels colored by fluoroscopy", table_cell_style), Paragraph("Integer [0 – 3 vessels]", table_cell_style), Paragraph("0 (No coronary vessel occlusion)", table_cell_style)],
        [Paragraph("<b>thal</b>", table_cell_style), Paragraph("Thallium stress test status", table_cell_style), Paragraph("Categorical [1, 2, 3]", table_cell_style), Paragraph("1: Normal, 2: Fixed defect, 3: Reversible", table_cell_style)]
    ]
    feat_table = Table(feat_rows, colWidths=[65, 145, 120, 174])
    feat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(feat_table)
    story.append(Spacer(1, 10))

    # ----------------- 4. PREPROCESSING -----------------
    story.append(Paragraph("4. Exploratory Data Analysis & Preprocessing Pipeline", h1_style))
    story.append(Paragraph(
        "A rigorous machine learning workflow requires thorough data validation to ensure stability and eliminate leakage:",
        body_style
    ))
    story.append(Paragraph("• <b>Target Alignment:</b> Explicitly aligned binary encoding so that <code>1 = Heart Disease / High Risk</code> and <code>0 = Healthy / Low Risk</code>, resolving raw dataset inversion.", bullet_style))
    story.append(Paragraph("• <b>Deduplication:</b> Checked and removed duplicate records, leaving 302 clean, verified patient samples.", bullet_style))
    story.append(Paragraph("• <b>Stratified 80/20 Partition:</b> Preserved natural class proportions across training (241 samples) and holdout test (61 samples) partitions.", bullet_style))
    story.append(Paragraph("• <b>StandardScaler Normalization:</b> Scaler was fitted strictly on <code>X_train</code> and applied to <code>X_test</code> to prevent data leakage.", bullet_style))

    # ----------------- 5. MODEL BENCHMARKING -----------------
    story.append(PageBreak()) # Clean page break for model benchmarks & charts
    story.append(Paragraph("5. Model Training & Algorithm Benchmarking", h1_style))
    story.append(Paragraph(
        "Five distinct classification algorithms were benchmarked under 5-Fold Stratified Cross-Validation on the training partition "
        "and evaluated against unseen holdout test data:",
        body_style
    ))

    bench_rows = [
        [Paragraph("Candidate Classifier", table_header_style), Paragraph("CV F1-Score", table_header_style), Paragraph("Accuracy", table_header_style), Paragraph("Precision", table_header_style), Paragraph("Recall (Sens.)", table_header_style), Paragraph("ROC-AUC", table_header_style)],
        [Paragraph("<b>Random Forest (Tuned)</b>", table_cell_style), Paragraph("<b>0.8673 ± 0.03</b>", table_cell_style), Paragraph("<b>81.97%</b>", table_cell_style), Paragraph("<b>77.50%</b>", table_cell_style), Paragraph("<b>93.94%</b>", table_cell_style), Paragraph("<b>0.9080</b>", table_cell_style)],
        [Paragraph("Support Vector Machine (SVC)", table_cell_style), Paragraph("0.8252 ± 0.04", table_cell_style), Paragraph("83.61%", table_cell_style), Paragraph("79.49%", table_cell_style), Paragraph("93.94%", table_cell_style), Paragraph("0.8810", table_cell_style)],
        [Paragraph("Gradient Boosting Classifier", table_cell_style), Paragraph("0.7841 ± 0.07", table_cell_style), Paragraph("81.97%", table_cell_style), Paragraph("80.56%", table_cell_style), Paragraph("87.88%", table_cell_style), Paragraph("0.8690", table_cell_style)],
        [Paragraph("K-Nearest Neighbors (KNN)", table_cell_style), Paragraph("0.8188 ± 0.04", table_cell_style), Paragraph("80.33%", table_cell_style), Paragraph("76.92%", table_cell_style), Paragraph("90.91%", table_cell_style), Paragraph("0.8674", table_cell_style)],
        [Paragraph("Logistic Regression", table_cell_style), Paragraph("0.8379 ± 0.05", table_cell_style), Paragraph("78.69%", table_cell_style), Paragraph("76.32%", table_cell_style), Paragraph("87.88%", table_cell_style), Paragraph("0.8647", table_cell_style)]
    ]
    bench_table = Table(bench_rows, colWidths=[130, 80, 70, 70, 84, 70])
    bench_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#DCFCE7")), # Highlight tuned winner
        ('ROWBACKGROUNDS', (0, 2), (-1, -1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(bench_table)
    story.append(Spacer(1, 10))

    # Embed Figure 1: Model Comparison
    comp_img = 'reports/plots/model_comparison.png'
    if os.path.exists(comp_img):
        story.append(Image(comp_img, width=470, height=220))
        story.append(Paragraph("Figure 1: Multi-metric cross-validation and test benchmark scores across 5 candidate classifiers.", caption_style))

    # ----------------- 6. HYPERPARAMETER TUNING & DIAGNOSTIC EVALUATION -----------------
    story.append(Paragraph("6. Hyperparameter Tuning & Diagnostic Evaluation", h1_style))
    story.append(Paragraph(
        "Using 5-Fold Stratified GridSearchCV across tree depth, estimator counts, and splitting constraints, the optimal Random Forest "
        "hyperparameters were selected (<code>n_estimators=100</code>, <code>max_depth=4</code>, <code>min_samples_leaf=3</code>, "
        "<code>min_samples_split=2</code>). This regularized ensemble achieved <b>93.94% Recall</b>, minimizing deadly false negatives.",
        body_style
    ))

    # Embed Confusion Matrix and ROC Curve side by side in a table
    cm_img = 'reports/plots/confusion_matrix.png'
    roc_img = 'reports/plots/roc_curve.png'
    if os.path.exists(cm_img) and os.path.exists(roc_img):
        diag_images = [
            [Image(cm_img, width=235, height=195), Image(roc_img, width=255, height=195)],
            [Paragraph("Figure 2: Holdout confusion matrix (31/33 disease cases detected).", caption_style),
             Paragraph("Figure 3: ROC Curve (Area Under Curve = 0.908).", caption_style)]
        ]
        diag_table = Table(diag_images, colWidths=[245, 259])
        diag_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(diag_table)

    # ----------------- 7. FEATURE IMPORTANCES & CLINICAL DRIVERS -----------------
    story.append(Paragraph("7. Predictive Biomarker Importance", h1_style))
    story.append(Paragraph(
        "Extracting Gini impurity reduction across the 100 decision trees reveals the physiological drivers of the model's predictions:",
        body_style
    ))
    fi_img = 'reports/plots/feature_importance.png'
    if os.path.exists(fi_img):
        story.append(Image(fi_img, width=460, height=210))
        story.append(Paragraph("Figure 4: Feature importance ranking indicating thal, ca, oldpeak, and exang as top coronary risk predictors.", caption_style))

    # ----------------- 8. SERIALIZATION: JOBLIB VS PICKLE -----------------
    story.append(PageBreak()) # Clean page break for deployment & testing
    story.append(Paragraph("8. Model Serialization: Joblib vs. Pickle Analysis", h1_style))
    story.append(Paragraph(
        "Bridging offline experimentation and live serving requires robust model serialization. "
        "Both Joblib and native Pickle were implemented and verified for inference parity:",
        body_style
    ))

    ser_rows = [
        [Paragraph("Dimension", table_header_style), Paragraph("Joblib (heart_disease_model.joblib)", table_header_style), Paragraph("Pickle (heart_disease_model.pkl)", table_header_style)],
        [Paragraph("<b>NumPy Optimization</b>", table_cell_style), Paragraph("Memory-mapped I/O optimized for large NumPy matrices", table_cell_style), Paragraph("Standard Python object stream serialization", table_cell_style)],
        [Paragraph("<b>File Size</b>", table_cell_style), Paragraph("~ 239 KB compact file", table_cell_style), Paragraph("~ 241 KB", table_cell_style)],
        [Paragraph("<b>Cold Load Time</b>", table_cell_style), Paragraph("~ 3.2 ms average cold load time", table_cell_style), Paragraph("~ 4.1 ms average load time", table_cell_style)],
        [Paragraph("<b>Production Status</b>", table_cell_style), Paragraph("Primary Scikit-Learn production serialization standard", table_cell_style), Paragraph("Native standard library fallback format", table_cell_style)]
    ]
    ser_table = Table(ser_rows, colWidths=[120, 192, 192])
    ser_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(ser_table)
    story.append(Spacer(1, 10))

    # ----------------- 9. WEB & API DEPLOYMENT -----------------
    story.append(Paragraph("9. Web Application & REST API Microservice Deployment", h1_style))
    story.append(Paragraph(
        "The deployment layer is engineered using Flask to provide dual access channels:",
        body_style
    ))
    story.append(Paragraph("• <b>Interactive Web Dashboard (<code>/</code> & <code>/predict</code>):</b> Modern, accessible interface featuring 1-click test sample loaders (Healthy Sample: <b>3.37% risk</b>; High-Risk Sample: <b>95.22% risk</b>), dynamic progress meters, and printable clinical diagnostic reports.", bullet_style))
    story.append(Paragraph("• <b>RESTful Prediction API (<code>POST /api/predict</code>):</b> Stateless JSON endpoint accepting 13 biomarkers and returning class predictions (0/1), probability percentages, risk tiers (Low/Moderate/High), and clinical advice.", bullet_style))
    story.append(Paragraph("• <b>Readiness & Metadata Probes (<code>/health</code> & <code>/api/models/info</code>):</b> Enables automated container orchestration and schema discovery.", bullet_style))

    # ----------------- 10. TESTING & VERIFICATION -----------------
    story.append(Paragraph("10. Automated Quality Assurance & Testing Suite", h1_style))
    story.append(Paragraph(
        "The automated test harness (<code>test_suite.py</code>) executes 11 unit and integration test cases covering all layers with a <b>100% pass rate</b>:",
        body_style
    ))

    test_rows = [
        [Paragraph("Test Module", table_header_style), Paragraph("Component Verified", table_header_style), Paragraph("Test Result", table_header_style)],
        [Paragraph("<code>test_preprocessing.py</code>", table_cell_style), Paragraph("Dataset presence, column schema validation, deduplication, and StandardScaler math", table_cell_style), Paragraph("<font color='#16A34A'><b>PASS (3/3)</b></font>", table_cell_style)],
        [Paragraph("<code>test_model.py</code>", table_cell_style), Paragraph("Joblib & Pickle prediction parity, probability bounds [0.0, 1.0]", table_cell_style), Paragraph("<font color='#16A34A'><b>PASS (2/2)</b></font>", table_cell_style)],
        [Paragraph("<code>test_api.py</code>", table_cell_style), Paragraph("HTTP 200 on /health, /api/models/info, /api/predict; HTTP 400 on missing payload keys; HTML rendering", table_cell_style), Paragraph("<font color='#16A34A'><b>PASS (6/6)</b></font>", table_cell_style)]
    ]
    test_table = Table(test_rows, colWidths=[140, 264, 100])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(test_table)
    story.append(Spacer(1, 10))

    # ----------------- 11. CONCLUSION -----------------
    story.append(Paragraph("11. Conclusion & Future Roadmap", h1_style))
    story.append(Paragraph(
        "CardioPredict AI represents a robust, clinically oriented application of applied machine learning. "
        "By optimizing for sensitivity (93.94% recall), the system prioritizes patient survival while providing transparent, "
        "sub-5ms inference. Planned future directions include integrating SHAP (Shapley Additive Explanations) for patient-specific "
        "decision attribution waterfall plots, Docker containerization for cloud scalability (AWS/GCP), and HL7/FHIR healthcare "
        "messaging compliance.",
        body_style
    ))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] PDF report compiled successfully to: {output_path}")


if __name__ == '__main__':
    build_pdf_report()
