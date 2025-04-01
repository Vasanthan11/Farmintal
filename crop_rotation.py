from flask import Blueprint, render_template, request, jsonify
import MySQLdb

crop_rotation_bp = Blueprint('crop_rotation', __name__)

# Database Connection
db = MySQLdb.connect(host="localhost", user="root", passwd="", db="crop_yield_db", charset="utf8mb4")
cursor = db.cursor()

# Route to display the crop rotation planner page
@crop_rotation_bp.route('/crop-rotation', methods=['GET'])
def crop_rotation():
    cursor.execute("SELECT DISTINCT state FROM crop_rotation")
    states = [row[0] for row in cursor.fetchall()]
    return render_template('crop_rotation.html', states=states)

# API to fetch district-wise crop rotation details for a selected state
@crop_rotation_bp.route('/get-rotation-data', methods=['POST'])
def get_rotation_data():
    state = request.form.get('state')  # Ensure we safely fetch form data
    
    cursor.execute("""
        SELECT district, current_crop, next_crop, recommended_rotation 
        FROM crop_rotation WHERE state = %s
    """, (state,))
    
    data = cursor.fetchall()

    # Ensure JSON response is formatted properly
    result = []
    for row in data:
        result.append({
            "district": row[0], 
            "current_crop": row[1], 
            "next_crop": row[2], 
            "recommended_rotation": row[3]
        })

    return jsonify(result)
