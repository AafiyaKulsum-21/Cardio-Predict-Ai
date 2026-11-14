// CardioPredict AI - Client interaction & dynamic assessment script

// Healthy patient profile (low BP, optimal lipid panel, no exercise angina, normal ECG)
const healthySample = {
    age: 45,
    sex: 0,        // Female
    cp: 1,         // Atypical angina
    trestbps: 118, // Normal BP (< 120 mm Hg)
    chol: 195,     // Optimal cholesterol (< 200 mg/dl)
    fbs: 0,        // Normal fasting sugar
    restecg: 0,    // Normal ECG
    thalach: 172,  // High stress heart rate
    exang: 0,      // No exercise angina
    oldpeak: 0.2,  // Normal ST depression (< 1 mm)
    slope: 2,      // Upsloping
    ca: 0,         // 0 vessels colored (clear)
    thal: 2        // Normal perfusion
};

// High-risk patient profile (advanced age, Stage 2 hypertension, hypercholesterolemia, severe ST depression, 2 blocked vessels)
const highRiskSample = {
    age: 63,
    sex: 1,        // Male
    cp: 0,         // Typical severe angina
    trestbps: 155, // Hypertension Stage 2
    chol: 288,     // High cholesterol (> 240 mg/dl)
    fbs: 1,        // Fasting glucose > 120
    restecg: 2,    // Left ventricular hypertrophy
    thalach: 115,  // Low max heart rate
    exang: 1,      // Exercise induced angina present
    oldpeak: 2.8,  // Severe ST depression (2.8 mm)
    slope: 1,      // Flat ST slope
    ca: 2,         // 2 major vessels occluded
    thal: 3        // Reversible perfusion defect
};

function loadSample(type) {
    const data = type === 'healthy' ? healthySample : highRiskSample;
    for (const key in data) {
        const input = document.getElementById(key);
        if (input) {
            input.value = data[key];
            // Highlight animation
            input.classList.add('input-highlight');
            setTimeout(() => input.classList.remove('input-highlight'), 600);
        }
    }
}

function resetForm() {
    document.getElementById('predictionForm').reset();
    const card = document.getElementById('instantResultCard');
    if (card) card.classList.add('d-none');
}

async function predictViaAjax() {
    const form = document.getElementById('predictionForm');
    const formData = new FormData(form);
    const payload = {};
    formData.forEach((val, key) => {
        payload[key] = parseFloat(val);
    });

    const instantCard = document.getElementById('instantResultCard');
    const instantDiagnosis = document.getElementById('instantDiagnosis');
    const instantBadge = document.getElementById('instantBadge');
    const instantDescription = document.getElementById('instantDescription');
    const instantProgressBar = document.getElementById('instantProgressBar');
    const instantScore = document.getElementById('instantScore');
    const instantIcon = document.getElementById('instantIcon');
    const instantRecs = document.getElementById('instantRecommendations');

    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (data.status === 'success') {
            instantCard.classList.remove('d-none');
            instantScore.innerText = `${data.probability}%`;
            instantProgressBar.style.width = `${data.probability}%`;
            instantProgressBar.innerText = `${data.probability}%`;

            // Reset classes
            instantBadge.className = 'badge fs-6 px-3 py-2 rounded-pill';
            instantProgressBar.className = 'progress-bar progress-bar-striped progress-bar-animated';
            instantIcon.className = 'result-icon-wrapper';

            if (data.risk_level === 'High Risk') {
                instantDiagnosis.innerText = 'High Risk: Heart Disease Indicated';
                instantDiagnosis.className = 'fw-bold mb-0 text-danger';
                instantBadge.classList.add('bg-danger', 'text-white');
                instantBadge.innerText = `High Risk (${data.probability}%)`;
                instantProgressBar.classList.add('bg-danger');
                instantIcon.classList.add('bg-danger-subtle', 'text-danger');
                instantIcon.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i>';
                instantDescription.innerText = `Strong ischemic cardiac risk indicated by the Random Forest model with an estimated probability of ${data.probability}%. Immediate clinical follow-up is recommended.`;
            } else if (data.risk_level === 'Moderate Risk') {
                instantDiagnosis.innerText = 'Moderate Risk Profile';
                instantDiagnosis.className = 'fw-bold mb-0 text-warning-emphasis';
                instantBadge.classList.add('bg-warning', 'text-dark');
                instantBadge.innerText = `Moderate Risk (${data.probability}%)`;
                instantProgressBar.classList.add('bg-warning');
                instantIcon.classList.add('bg-warning-subtle', 'text-warning-emphasis');
                instantIcon.innerHTML = '<i class="fa-solid fa-circle-exclamation"></i>';
                instantDescription.innerText = `Borderline cardiovascular parameters observed (${data.probability}% risk score). Preventive cardiometabolic consultation and lifestyle adjustments advised.`;
            } else {
                instantDiagnosis.innerText = 'Low Risk: Healthy Cardiovascular Baseline';
                instantDiagnosis.className = 'fw-bold mb-0 text-success';
                instantBadge.classList.add('bg-success', 'text-white');
                instantBadge.innerText = `Low Risk (${data.probability}%)`;
                instantProgressBar.classList.add('bg-success');
                instantIcon.classList.add('bg-success-subtle', 'text-success');
                instantIcon.innerHTML = '<i class="fa-solid fa-heart-circle-check"></i>';
                instantDescription.innerText = `Evaluated physiological indicators fall within healthy reference boundaries (only ${data.probability}% calculated disease probability).`;
            }

            instantRecs.innerHTML = '';
            if (data.recommendations && data.recommendations.length > 0) {
                data.recommendations.forEach(r => {
                    const li = document.createElement('li');
                    li.className = 'list-group-item px-0 py-2 d-flex align-items-center gap-2 border-0';
                    li.innerHTML = `<i class="fa-solid fa-check text-primary"></i> <span><strong>${r.title}:</strong> ${r.description}</span>`;
                    instantRecs.appendChild(li);
                });
            }

            instantCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            alert('Prediction error: ' + (data.message || 'Unknown error'));
        }
    } catch (err) {
        console.error('API Error:', err);
        alert('Failed to connect to the prediction API service. Ensure Flask server is running.');
    }
}
