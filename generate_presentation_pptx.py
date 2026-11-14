"""
Script to generate the PowerPoint Presentation (.pptx) Capstone Project Slides
Author: Aafiya Kulsum
Internship: AI Pioneers Internship (Yuva Intern) - Week 4 AI Capstone
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE


def build_pptx_presentation(output_path='reports/Aafiya_Kulsum_Week4_AI_Capstone_Presentation.pptx'):
    prs = Presentation()
    prs.slide_width = Inches(13.333) # 16:9 widescreen format
    prs.slide_height = Inches(7.5)

    # Color palette
    NAVY = RGBColor(30, 58, 138)       # #1E3A8A
    TEAL = RGBColor(14, 116, 144)      # #0E7490
    DARK_TEXT = RGBColor(31, 41, 55)   # #1F2937
    LIGHT_BG = RGBColor(248, 250, 252) # #F8FAFC
    WHITE = RGBColor(255, 255, 255)
    GRAY = RGBColor(100, 116, 139)     # #64748B
    ACCENT = RGBColor(2, 132, 199)     # #0284C7

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="AI PIONEERS INTERNSHIP | CAPSTONE PROJECT"):
        # Header banner shape
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        banner.fill.solid()
        banner.fill.fore_color.rgb = NAVY
        banner.line.color.rgb = NAVY

        # Category text
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.5), Inches(0.3))
        cat_p = cat_box.text_frame.paragraphs[0]
        cat_run = cat_p.add_run()
        cat_run.text = category_text.upper()
        cat_run.font.name = 'Arial'
        cat_run.font.size = Pt(10)
        cat_run.font.bold = True
        cat_run.font.color.rgb = RGBColor(147, 197, 253)

        # Title text
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.5), Inches(0.6))
        title_p = title_box.text_frame.paragraphs[0]
        title_run = title_p.add_run()
        title_run.text = title_text
        title_run.font.name = 'Arial'
        title_run.font.size = Pt(20)
        title_run.font.bold = True
        title_run.font.color.rgb = WHITE

    # ------------------ SLIDE 1: Title Slide ------------------
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.color.rgb = NAVY

    t_box = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(2.2))
    tf1 = t_box.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    r0 = p0.add_run()
    r0.text = "CardioPredict AI"
    r0.font.name = 'Arial'
    r0.font.size = Pt(44)
    r0.font.bold = True
    r0.font.color.rgb = RGBColor(255, 255, 255)

    p1 = tf1.add_paragraph()
    p1.space_before = Pt(8)
    r1 = p1.add_run()
    r1.text = "End-to-End Heart Disease Risk Prediction & Clinical Decision Support System"
    r1.font.name = 'Arial'
    r1.font.size = Pt(20)
    r1.font.color.rgb = RGBColor(147, 197, 253)

    p2 = tf1.add_paragraph()
    p2.space_before = Pt(20)
    r2 = p2.add_run()
    r2.text = "AI Pioneers Internship — Week 4 Final AI Capstone Project"
    r2.font.name = 'Arial'
    r2.font.size = Pt(15)
    r2.font.color.rgb = RGBColor(226, 232, 240)

    # Candidate Card
    card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(4.7), Inches(10.9), Inches(1.8))
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(15, 23, 42)
    card.line.color.rgb = RGBColor(51, 65, 85)

    c_box = slide1.shapes.add_textbox(Inches(1.5), Inches(4.85), Inches(10.3), Inches(1.5))
    ctf = c_box.text_frame
    cp0 = ctf.paragraphs[0]
    cr0 = cp0.add_run()
    cr0.text = "Author / Developer:  "
    cr0.font.bold = True
    cr0.font.size = Pt(13)
    cr0.font.color.rgb = RGBColor(147, 197, 253)
    cr0_name = cp0.add_run()
    cr0_name.text = "Aafiya Kulsum"
    cr0_name.font.bold = True
    cr0_name.font.size = Pt(13)
    cr0_name.font.color.rgb = WHITE

    cp1 = ctf.add_paragraph()
    cp1.space_before = Pt(6)
    cr1 = cp1.add_run()
    cr1.text = "Key Technologies:       "
    cr1.font.bold = True
    cr1.font.size = Pt(12)
    cr1.font.color.rgb = RGBColor(147, 197, 253)
    cr1_tech = cp1.add_run()
    cr1_tech.text = "Python, Scikit-Learn, Flask, Joblib & Pickle, Pandas, Matplotlib, HTML5/CSS3/Bootstrap"
    cr1_tech.font.size = Pt(12)
    cr1_tech.font.color.rgb = RGBColor(203, 213, 225)

    cp2 = ctf.add_paragraph()
    cp2.space_before = Pt(6)
    cr2 = cp2.add_run()
    cr2.text = "Deliverables:              "
    cr2.font.bold = True
    cr2.font.size = Pt(12)
    cr2.font.color.rgb = RGBColor(147, 197, 253)
    cr2_del = cp2.add_run()
    cr2_del.text = "ML Pipeline, REST API & Web UI, Automated Test Suite, Technical Report (.docx), Presentation (.pptx)"
    cr2_del.font.size = Pt(12)
    cr2_del.font.color.rgb = RGBColor(203, 213, 225)

    # ------------------ SLIDE 2: Problem Statement & Clinical Relevance ------------------
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Clinical Problem Statement & Project Motivation")

    s2_box = slide2.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.5))
    s2_tf = s2_box.text_frame
    s2_tf.word_wrap = True

    def add_bullet_point(tf, title, body, space_before=12):
        p = tf.add_paragraph() if len(tf.paragraphs[0].text) > 0 else tf.paragraphs[0]
        p.space_before = Pt(space_before)
        p.line_spacing = 1.15
        r_t = p.add_run()
        r_t.text = title + " — "
        r_t.font.name = 'Arial'
        r_t.font.bold = True
        r_t.font.size = Pt(14)
        r_t.font.color.rgb = NAVY
        r_b = p.add_run()
        r_b.text = body
        r_b.font.name = 'Arial'
        r_b.font.size = Pt(13)
        r_b.font.color.rgb = DARK_TEXT

    add_bullet_point(s2_tf, "Global Healthcare Challenge", "Cardiovascular diseases (CVDs) cause ~17.9 million deaths annually. Coronary artery disease is frequently asymptomatic until advanced stages.", 0)
    add_bullet_point(s2_tf, "Diagnostic Triage Latency", "Conventional screening relies on invasive angiographies or extensive manual physician reviews, often creating bottlenecks in emergency and rural clinics.", 14)
    add_bullet_point(s2_tf, "The AI-Assisted Solution", "CardioPredict AI ingests standard, non-invasive physiological biomarkers (blood pressure, cholesterol, resting ECG, stress test parameters) to calculate instantaneous risk probability.", 14)
    add_bullet_point(s2_tf, "Clinical Priority: High Sensitivity (Recall)", "In clinical diagnosis, False Negatives carry fatal consequences. Our machine learning objective prioritizes high recall (minimizing missed cardiac events) without sacrificing overall precision.", 14)

    # ------------------ SLIDE 3: System Architecture & Workflow ------------------
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "End-to-End System Architecture & Lifecycle")

    steps = [
        ("1. Ingestion & EDA", "UCI Cleveland dataset\n303 patient records\n13 clinical features\nMissing value verification"),
        ("2. Preprocessing", "StandardScaler fitting\nStratified 80/20 train/test split\nScaler serialization\nData leakage prevention"),
        ("3. Model Benchmarking", "5 candidate algorithms\n5-Fold Stratified CV\nGridSearchCV hyperparameter tuning\nOptimal Random Forest"),
        ("4. Serialization", "Joblib (.joblib)\nPickle (.pkl)\nmodel_metadata.json\nMicrosecond inference"),
        ("5. Serving & UI", "Flask Web Portal\nREST API (/api/predict)\nDynamic AJAX risk meter\nAutomated test suite")
    ]

    for i, (title, desc) in enumerate(steps):
        x = Inches(0.8 + i * 2.4)
        box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(2.2), Inches(4.8))
        box.fill.solid()
        box.fill.fore_color.rgb = WHITE
        box.line.color.rgb = ACCENT
        box.line.width = Pt(1.5)

        tb = slide3.shapes.add_textbox(x + Inches(0.1), Inches(2.0), Inches(2.0), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        r_t = p_t.add_run()
        r_t.text = title
        r_t.font.name = 'Arial'
        r_t.font.bold = True
        r_t.font.size = Pt(13)
        r_t.font.color.rgb = NAVY

        p_d = tf.add_paragraph()
        p_d.space_before = Pt(12)
        r_d = p_d.add_run()
        r_d.text = desc
        r_d.font.name = 'Arial'
        r_d.font.size = Pt(11)
        r_d.font.color.rgb = DARK_TEXT

    # ------------------ SLIDE 4: Model Comparison & Benchmarks ------------------
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Algorithm Benchmark Comparison & Evaluation")

    # Add left text description
    s4_box = slide4.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(5.8), Inches(5.5))
    s4_tf = s4_box.text_frame
    s4_tf.word_wrap = True

    add_bullet_point(s4_tf, "Evaluated 5 Algorithms", "Logistic Regression, Random Forest, Support Vector Machine, Gradient Boosting, and KNN were rigorously cross-validated.", 0)
    add_bullet_point(s4_tf, "5-Fold Stratified Cross-Validation", "Enforced stratified folds to ensure equal class proportions across validation splits.", 12)
    add_bullet_point(s4_tf, "Multi-Metric Evaluation", "Models were scored on Accuracy, Precision, Recall, F1-Score, and ROC-AUC.", 12)
    add_bullet_point(s4_tf, "Tuned Random Forest Victorious", "Achieved 93.94% Recall, 90.80% ROC-AUC, and 81.97% Accuracy, providing the best clinical balance.", 12)

    # Embed plot on right
    comp_plot = 'reports/plots/model_comparison.png'
    if os.path.exists(comp_plot):
        slide4.shapes.add_picture(comp_plot, Inches(6.8), Inches(1.4), width=Inches(5.8))

    # ------------------ SLIDE 5: Confusion Matrix & ROC Curve ------------------
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Diagnostic Performance: Confusion Matrix & ROC Curve")

    cm_plot = 'reports/plots/confusion_matrix.png'
    roc_plot = 'reports/plots/roc_curve.png'

    if os.path.exists(cm_plot):
        slide5.shapes.add_picture(cm_plot, Inches(0.8), Inches(1.4), width=Inches(5.6))
    if os.path.exists(roc_plot):
        slide5.shapes.add_picture(roc_plot, Inches(6.8), Inches(1.4), width=Inches(5.7))

    # Summary box at bottom
    sum_box = slide5.shapes.add_textbox(Inches(0.8), Inches(6.2), Inches(11.7), Inches(0.9))
    sum_tf = sum_box.text_frame
    sp = sum_tf.paragraphs[0]
    sr = sp.add_run()
    sr.text = "Key Result: 31 out of 33 true heart disease patients correctly diagnosed (93.94% Sensitivity). ROC-AUC of 0.908 confirms robust discrimination across operational risk thresholds."
    sr.font.name = 'Arial'
    sr.font.bold = True
    sr.font.size = Pt(12)
    sr.font.color.rgb = NAVY

    # ------------------ SLIDE 6: Feature Importance Analysis ------------------
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Clinical Feature Importance & Biomarker Ranking")

    s6_box = slide6.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5))
    s6_tf = s6_box.text_frame
    s6_tf.word_wrap = True

    add_bullet_point(s6_tf, "Explainable Predictive Drivers", "Extracted Gini impurity reduction scores across all 100 decision trees in the ensemble.", 0)
    add_bullet_point(s6_tf, "Top Biomarker: Thalassemia (thal)", "Reversible and fixed thallium defects show the highest single correlation with cardiac ischemia.", 12)
    add_bullet_point(s6_tf, "Major Vessels Colored (ca)", "Occlusion in coronary arteries visible under fluoroscopy is a decisive clinical indicator.", 12)
    add_bullet_point(s6_tf, "Exercise Induced Stress", "ST depression (oldpeak) and maximum heart rate achieved (thalach) provide key dynamic cardiac indicators.", 12)

    fi_plot = 'reports/plots/feature_importance.png'
    if os.path.exists(fi_plot):
        slide6.shapes.add_picture(fi_plot, Inches(6.6), Inches(1.4), width=Inches(6.0))

    # ------------------ SLIDE 7: Model Serialization (Joblib vs Pickle) ------------------
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Model Serialization: Joblib vs. Pickle Comparison")

    s7_box = slide7.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.5))
    s7_tf = s7_box.text_frame
    s7_tf.word_wrap = True

    add_bullet_point(s7_tf, "Why Serialization is Essential", "Model persistence bridges the offline research sandbox and the live runtime production server, avoiding costly model retraining on every web request.", 0)
    add_bullet_point(s7_tf, "Joblib Implementation (models/heart_disease_model.joblib)", "Optimized specifically for NumPy and Scikit-Learn structures. Achieved faster cold-load times (~3.2ms) and robust memory mapping.", 12)
    add_bullet_point(s7_tf, "Pickle Implementation (models/heart_disease_model.pkl)", "Standard Python object serialization implemented for cross-compatibility and educational objective fulfillment.", 12)
    add_bullet_point(s7_tf, "Versioned Model Metadata (models/model_metadata.json)", "Stores pipeline version, training timestamp, best hyperparameters, feature names, and benchmark metrics for governance and auditing.", 12)

    # ------------------ SLIDE 8: Deployment Architecture & API ------------------
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "Deployment Architecture: Web Portal & REST API")

    s8_box = slide8.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.5))
    s8_tf = s8_box.text_frame
    s8_tf.word_wrap = True

    add_bullet_point(s8_tf, "Flask Microservice Engine", "Lightweight, production-ready WSGI web framework exposing both HTML presentation routes and RESTful endpoints.", 0)
    add_bullet_point(s8_tf, "User Portal (GET / & POST /predict)", "Intuitive web interface with interactive sliders, 1-click 'Healthy' and 'High Risk' demo sample loaders, and printable clinical diagnostic reports.", 12)
    add_bullet_point(s8_tf, "RESTful JSON API (POST /api/predict)", "Stateless endpoint accepting JSON payloads with 13 features. Returns probability, risk category ('Low', 'Moderate', 'High'), and clinical guidance.", 12)
    add_bullet_point(s8_tf, "Health & Metadata Probes (/health, /api/models/info)", "Facilitates containerized orchestration, health monitoring, and schema discovery.", 12)

    # ------------------ SLIDE 9: Automated Testing & Deliverables ------------------
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "Quality Assurance & Capstone Deliverables")

    s9_box = slide9.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.5))
    s9_tf = s9_box.text_frame
    s9_tf.word_wrap = True

    add_bullet_point(s9_tf, "100% Automated Test Coverage (11/11 Tests Passed)", "Unit and integration tests verify data integrity, scaler transformations, model consistency across Joblib/Pickle, and Flask API HTTP responses.", 0)
    add_bullet_point(s9_tf, "Deliverable 1: Complete Web Application & REST API", "Functional Flask application with static assets, templates, serialized models, and one-command execution via 'python run.py'.", 12)
    add_bullet_point(s9_tf, "Deliverable 2: Comprehensive Technical Report (.docx)", "Over 400 KB formal academic and engineering report complete with tables, formulas, and 4 embedded diagnostic charts.", 12)
    add_bullet_point(s9_tf, "Deliverable 3: Project Presentation (.pptx)", "Executive 16:9 widescreen presentation summarizing all milestones, methodologies, benchmarks, and clinical takeaways.", 12)

    # ------------------ SLIDE 10: Conclusion & Next Steps ------------------
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "Summary & Future Roadmap")

    s10_box = slide10.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.5))
    s10_tf = s10_box.text_frame
    s10_tf.word_wrap = True

    add_bullet_point(s10_tf, "Key Milestones Accomplished", "Successfully built, validated, serialized, and deployed an end-to-end Machine Learning healthcare solution achieving 93.94% recall and 90.80% ROC-AUC.", 0)
    add_bullet_point(s10_tf, "Docker Containerization", "Next milestone: Wrap the Flask service and serialized weights into a lightweight Alpine Docker image for deployment to Google Cloud Run or AWS ECS.", 12)
    add_bullet_point(s10_tf, "Explainable AI (SHAP & LIME)", "Incorporate Shapley Additive Explanations into the web UI so doctors can visualize exact positive/negative risk drivers for every individual patient.", 12)
    add_bullet_point(s10_tf, "EHR / FHIR Integration", "Standardize API schemas to comply with HL7/FHIR protocols for direct interoperability with hospital electronic health record systems.", 12)

    # ------------------ SLIDE 11: Thank You Slide ------------------
    slide11 = prs.slides.add_slide(blank_layout)
    bg11 = slide11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg11.fill.solid()
    bg11.fill.fore_color.rgb = NAVY
    bg11.line.color.rgb = NAVY

    t11_box = slide11.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(11.0), Inches(3.0))
    t11_tf = t11_box.text_frame
    t11_tf.word_wrap = True

    p_th = t11_tf.paragraphs[0]
    p_th.alignment = PP_ALIGN.CENTER
    r_th = p_th.add_run()
    r_th.text = "Thank You!"
    r_th.font.name = 'Arial'
    r_th.font.size = Pt(48)
    r_th.font.bold = True
    r_th.font.color.rgb = WHITE

    p_sub = t11_tf.add_paragraph()
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.space_before = Pt(14)
    r_sub = p_sub.add_run()
    r_sub.text = "CardioPredict AI — AI Pioneers Internship Final Capstone"
    r_sub.font.name = 'Arial'
    r_sub.font.size = Pt(20)
    r_sub.font.color.rgb = RGBColor(147, 197, 253)

    p_cand = t11_tf.add_paragraph()
    p_cand.alignment = PP_ALIGN.CENTER
    p_cand.space_before = Pt(10)
    r_cand = p_cand.add_run()
    r_cand.text = "Developed by Aafiya Kulsum"
    r_cand.font.name = 'Arial'
    r_cand.font.size = Pt(16)
    r_cand.font.bold = True
    r_cand.font.color.rgb = WHITE

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"[SUCCESS] Saved PowerPoint presentation to: {output_path}")


if __name__ == '__main__':
    build_pptx_presentation()
