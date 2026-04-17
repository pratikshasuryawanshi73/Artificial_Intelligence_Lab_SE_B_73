// UI interactions and Modals
function openModal(modalId) {
    document.getElementById(modalId).classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

// Close modal when clicking outside
document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
        if(e.target === overlay) {
            overlay.classList.remove('active');
        }
    });
});

// Forms
const irrigationForm = document.getElementById('irrigationForm');
if(irrigationForm) {
    irrigationForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            crop_id: document.getElementById('irr_crop_id').value,
            date: document.getElementById('irr_date').value,
            duration_minutes: document.getElementById('irr_duration').value,
            water_amount: document.getElementById('irr_water').value
        };
        await postData('/api/irrigation', data);
        window.location.reload();
    });
}

const chemicalForm = document.getElementById('chemicalForm');
if(chemicalForm) {
    chemicalForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            crop_id: document.getElementById('chem_crop_id').value,
            chem_type: document.getElementById('chem_type').value,
            name: document.getElementById('chem_name').value,
            application_date: document.getElementById('chem_date').value,
            quantity: document.getElementById('chem_quantity').value
        };
        await postData('/api/chemicals', data);
        window.location.reload();
    });
}

const addCropForm = document.getElementById('addCropForm');
if(addCropForm) {
    addCropForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            name: document.getElementById('crop_name').value,
            category: document.getElementById('crop_category').value,
            planted_date: document.getElementById('crop_planted_date').value,
            expected_harvest_date: document.getElementById('crop_harvest_date').value
        };
        await postData('/api/crops', data);
        window.location.reload();
    });
}

// Mark irrigation as done
async function markDone(scheduleId) {
    await fetch(`/api/mark_irrigation_done/${scheduleId}`, { method: 'POST' });
    window.location.reload();
}

// API Helper
async function postData(url, data) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        if(!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        alert("Failed to save data. Please check if Crop ID exists.");
    }
}

// Set minimum date for input fields to prevent past dates
document.addEventListener('DOMContentLoaded', () => {
    const today = new Date().toISOString().split('T')[0];
    
    // Dynamic Greeting
    const greetingEl = document.getElementById('dynamicGreeting');
    if (greetingEl) {
        const hour = new Date().getHours();
        let greetingMsg = 'Good Evening, Farmer!';
        if (hour < 12) greetingMsg = 'Good Morning, Farmer!';
        else if (hour < 18) greetingMsg = 'Good Afternoon, Farmer!';
        greetingEl.textContent = greetingMsg;
    }

    // For Schedule Irrigation
    const irrDateInput = document.getElementById('irr_date');
    if (irrDateInput) {
        irrDateInput.setAttribute('min', today);
    }

    // Load Charts if canvases exist
    if (document.getElementById('cropChart')) {
        loadAnalytics();
    }
});

async function loadAnalytics() {
    try {
        const response = await fetch('/api/analytics');
        const data = await response.json();
        
        // 1. Crop Categories (Doughnut)
        const cropCtx = document.getElementById('cropChart').getContext('2d');
        new Chart(cropCtx, {
            type: 'doughnut',
            data: {
                labels: data.crop_categories.map(c => c.category),
                datasets: [{
                    label: 'Crops',
                    data: data.crop_categories.map(c => c.count),
                    backgroundColor: ['#059669', '#10B981', '#34D399', '#6EE7B7', '#A7F3D0'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { 
                    title: { display: true, text: 'Crops by Category', font: { family: "'Outfit', sans-serif" } },
                    legend: { position: 'bottom' }
                }
            }
        });
        
        // 2. Water Usage Trends (Line)
        const waterCtx = document.getElementById('waterChart').getContext('2d');
        new Chart(waterCtx, {
            type: 'line',
            data: {
                labels: data.water_trends.map(w => w.date),
                datasets: [{
                    label: 'Water Used (Liters)',
                    data: data.water_trends.map(w => w.total_water),
                    borderColor: '#3B82F6', backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    fill: true, tension: 0.4
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { 
                    title: { display: true, text: 'Water Usage Trend', font: { family: "'Outfit', sans-serif" } },
                    legend: { display: false }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
        
        // 3. Chemical Usage (Bar)
        const chemCtx = document.getElementById('chemChart').getContext('2d');
        new Chart(chemCtx, {
            type: 'bar',
            data: {
                labels: data.chem_trends.map(c => c.chem_type),
                datasets: [{
                    label: 'Quantity (kg/L)',
                    data: data.chem_trends.map(c => c.total_qty),
                    backgroundColor: ['#F59E0B', '#EF4444'],
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { 
                    title: { display: true, text: 'Chemical Usage Totals', font: { family: "'Outfit', sans-serif" } },
                    legend: { display: false } 
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
        
    } catch(err) {
        console.error("Failed to load analytics: ", err);
    }
}
