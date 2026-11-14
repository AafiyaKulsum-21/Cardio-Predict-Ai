// CardioPredict AI - Client-side interaction & API testing script

const healthySample = {
    age: 45,
    sex: 0,
    cp: 1,
    trestbps: 118,
    chol: 195,
    fbs: 0,
    restecg: 0,
    thalach: 172,
    exang: 0,
    oldpeak: 0.2,
    slope: 2,
    ca: 0,
    thal: 2
};

const highRiskSample = {
    age: 63,
    sex: 1,
    cp: 0,
    trestbps: 155,
    chol: 288,
    fbs: 1,
    restecg: 2,
    thalach: 115,
    exang: 1,
    oldpeak: 2.8,
    slope: 1,
    ca: 2,
    thal: 3
};

function loadSample(type) {
    const data = type === 'healthy' ? healthySample : highRiskSample;
    for (const key in data) {
        const input = document.getElementById(key);
        if (input) {
            input.value = data[key];
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
    const instantTitle = document.getElementById('instantTitle');
    const instantBadge = document.getElementById('instantBadge');
    const instantAlert = document.getElementById('instantAlert');
    const instantDiagnosis = document.getElementById('instantDiagnosis');
    const instantDescription = document.getElementById('instantDescription');
    const instantProgressBar = document.getElementById('instantProgressBar');
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
            instantTitle.innerText = `Diagnosis: ${data.diagnosis}`;
            instantBadge.innerText = `Risk Level: ${data.risk_level} (${data.probability}%)`;

            // Reset styles
            instantAlert.className = 'alert mb-3';
            instantBadge.className = 'badge';
            instantProgressBar.className = 'progress-bar progress-bar-striped progress-bar-animated';

            if (data.risk_level === 'High Risk') {
                instantAlert.classList.add('alert-danger');
                instantBadge.classList.add('bg-danger');
                instantProgressBar.classList.add('bg-danger');
            } else if (data.risk_level === 'Moderate Risk') {
                instantAlert.classList.add('alert-warning');
                instantBadge.classList.add('bg-warning', 'text-dark');
                instantProgressBar.classList.add('bg-warning');
            } else {
                instantAlert.classList.add('alert-success');
                instantBadge.classList.add('bg-success');
                instantProgressBar.classList.add('bg-success');
            }

            instantDiagnosis.innerText = data.diagnosis;
            instantDescription.innerText = `The Random Forest model evaluated this profile with an estimated coronary heart disease probability of ${data.probability}%.`;
            instantProgressBar.style.width = `${data.probability}%`;
            instantProgressBar.innerText = `${data.probability}%`;

            instantRecs.innerHTML = '';
            if (data.recommendations && data.recommendations.length > 0) {
                data.recommendations.forEach(r => {
                    const li = document.createElement('li');
                    li.className = 'list-group-item px-0 py-2 d-flex align-items-center gap-2';
                    li.innerHTML = `<i class="fa-solid fa-check text-primary"></i> <strong>${r.title}:</strong> ${r.description}`;
                    instantRecs.appendChild(li);
                });
            }

            instantCard.scrollIntoView({ behavior: 'smooth' });
        } else {
            alert('Prediction error: ' + (data.message || 'Unknown error'));
        }
    } catch (err) {
        console.error('Error invoking prediction API:', err);
        alert('Failed to connect to the prediction API service. Check server console.');
    }
}
