// Theme Park Accessibility Planner - Frontend JavaScript

document.getElementById('queryForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const parkName = document.getElementById('parkName').value;
    const dietaryRestrictions = document.getElementById('dietaryRestrictions').value;
    const allergens = document.getElementById('allergens').value;

    if (!parkName) {
        showError('Please select a theme park');
        return;
    }

    // Show loading, hide form and plan
    showLoading();
    hideError();

    try {
        const response = await fetch('/api/generate-plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                park_name: parkName,
                dietary_restrictions: dietaryRestrictions,
                allergens: allergens
            })
        });

        const data = await response.json();

        if (!response.ok) {
            showError(data.error || 'Failed to generate plan');
            return;
        }

        // Display the plan
        displayPlan(data);
    } catch (error) {
        showError(`Error: ${error.message}`);
    }
});

function displayPlan(data) {
    hideLoading();

    // Build park info section
    const parkInfo = document.getElementById('parkInfo');
    let infoHTML = `<h3>${data.park}</h3>`;
    
    if (data.dietary_restrictions.length > 0) {
        infoHTML += `<p><strong>Dietary Restrictions:</strong> ${data.dietary_restrictions.join(', ')}</p>`;
    }
    
    if (data.allergens.length > 0) {
        infoHTML += `<p><strong>Allergens to Avoid:</strong> ${data.allergens.join(', ')}</p>`;
    }

    parkInfo.innerHTML = infoHTML;

    // Display the plan
    const planContent = document.getElementById('planContent');
    planContent.innerHTML = `<pre>${escapeHtml(data.plan)}</pre>`;

    // Show the plan container
    document.getElementById('planContainer').classList.remove('hidden');

    // Scroll to plan
    setTimeout(() => {
        document.getElementById('planContainer').scrollIntoView({ behavior: 'smooth' });
    }, 100);
}

function showLoading() {
    document.getElementById('queryForm').classList.add('hidden');
    document.getElementById('loading').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('queryForm').classList.remove('hidden');
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
    hideLoading();
}

function hideError() {
    document.getElementById('error').classList.add('hidden');
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
