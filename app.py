from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import fetch_all, fetch_one, execute_query

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Fetch summary data
    crops_count = fetch_one("SELECT COUNT(*) as count FROM crops")['count']
    growing_count = fetch_one("SELECT COUNT(*) as count FROM crops WHERE status = 'growing'")['count']
    
    # Upcoming irrigation schedules
    schedules = fetch_all("""
        SELECT i.*, c.name as crop_name 
        FROM irrigation_schedules i 
        JOIN crops c ON i.crop_id = c.id 
        WHERE i.status = 'scheduled' 
        ORDER BY i.date ASC LIMIT 5
    """)
    
    recent_logs = fetch_all("""
        SELECT l.*, c.name as crop_name 
        FROM chemical_logs l 
        JOIN crops c ON l.crop_id = c.id 
        ORDER BY l.application_date DESC LIMIT 5
    """)
    
    return render_template('dashboard.html', 
                           crops_count=crops_count, 
                           growing_count=growing_count,
                           schedules=schedules,
                           recent_logs=recent_logs)

@app.route('/api/crops', methods=['GET', 'POST'])
def api_crops():
    if request.method == 'POST':
        data = request.json
        query = "INSERT INTO crops (name, category, planted_date, expected_harvest_date) VALUES (%s, %s, %s, %s)"
        execute_query(query, (data['name'], data['category'], data['planted_date'], data['expected_harvest_date']))
        return jsonify({"message": "Crop added successfully"}), 201
    
    crops = fetch_all("SELECT * FROM crops ORDER BY planted_date DESC")
    return jsonify(crops)

@app.route('/crops')
def crops_page():
    crops = fetch_all("SELECT * FROM crops ORDER BY planted_date DESC")
    return render_template('crops.html', crops=crops)

@app.route('/api/irrigation', methods=['POST'])
def api_irrigation():
    data = request.json
    query = "INSERT INTO irrigation_schedules (crop_id, date, duration_minutes, water_amount) VALUES (%s, %s, %s, %s)"
    execute_query(query, (data['crop_id'], data['date'], data['duration_minutes'], data['water_amount']))
    return jsonify({"message": "Schedule added"}), 201

@app.route('/api/chemicals', methods=['POST'])
def api_chemicals():
    data = request.json
    query = "INSERT INTO chemical_logs (crop_id, chem_type, name, application_date, quantity) VALUES (%s, %s, %s, %s, %s)"
    execute_query(query, (data['crop_id'], data['chem_type'], data['name'], data['application_date'], data['quantity']))
    return jsonify({"message": "Chemical log added"}), 201

@app.route('/api/mark_irrigation_done/<int:schedule_id>', methods=['POST'])
def mark_irrigation_done(schedule_id):
    execute_query("UPDATE irrigation_schedules SET status = 'completed' WHERE id = %s", (schedule_id,))
    return jsonify({"message": "Updated"}), 200

@app.route('/api/analytics')
def api_analytics():
    # Crop Categories
    crop_categories = fetch_all("SELECT category, COUNT(*) as count FROM crops GROUP BY category")
    
    # Water usage trends
    water_trends = fetch_all("SELECT date, SUM(water_amount) as total_water FROM irrigation_schedules WHERE status = 'completed' GROUP BY date ORDER BY date DESC LIMIT 7")
    
    # Chemical trends
    chem_trends = fetch_all("SELECT chem_type, SUM(quantity) as total_qty FROM chemical_logs GROUP BY chem_type")
    
    return jsonify({
        "crop_categories": crop_categories,
        "water_trends": water_trends[::-1],
        "chem_trends": chem_trends
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
