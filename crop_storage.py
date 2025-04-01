from flask import Blueprint, render_template, request, jsonify
import MySQLdb

crop_storage_bp = Blueprint('crop_storage', __name__)

# Database Connection
db = MySQLdb.connect(host="localhost", user="root", passwd="", db="crop_yield_db")
cursor = db.cursor()

# Route to display crop storage page
@crop_storage_bp.route('/crop-storage')
def crop_storage():
    cursor.execute("SELECT DISTINCT state FROM crop_storage")
    states = [row[0] for row in cursor.fetchall()]
    return render_template('crop_storage.html', states=states)

# API to fetch district-wise crop storage details for a selected state
@crop_storage_bp.route('/get-crop-data', methods=['POST'])
def get_crop_data():
    state = request.form['state']
    cursor.execute("SELECT district, crop_name, stored_tons, required_tons, time_limit FROM crop_storage WHERE state = %s", (state,))
    data = cursor.fetchall()
    result = [{"district": row[0], "crop_name": row[1], "stored_tons": row[2], "required_tons": row[3], "time_limit": row[4]} for row in data]
    return jsonify(result)
