from flask import Blueprint, render_template, request, jsonify
import MySQLdb

# Create Blueprint
irrigation_bp = Blueprint('irrigation', __name__)

# Database Connection
db = MySQLdb.connect(host="localhost", user="root", passwd="", db="crop_yield_db")
cursor = db.cursor()

# Route to display the irrigation page
@irrigation_bp.route('/irrigation', methods=['GET'])
def irrigation():
    cursor.execute("SELECT DISTINCT state FROM irrigation_data")
    states = [row[0] for row in cursor.fetchall()]
    return render_template('irrigation.html', states=states)

# API to fetch irrigation data based on selected state
@irrigation_bp.route('/get-irrigation-data', methods=['POST'])
def get_irrigation_data():
    state = request.form.get('state')

    cursor.execute("SELECT district, crop, ideal_moisture_range, irrigation_frequency, recommended_irrigation FROM irrigation_data WHERE state = %s", (state,))
    data = cursor.fetchall()

    result = [{
        "district": row[0],
        "crop": row[1],
        "ideal_moisture_range": row[2],
        "irrigation_frequency": row[3],
        "recommended_irrigation": row[4]
    } for row in data]

    return jsonify(result)
