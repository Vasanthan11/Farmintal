from flask import Blueprint, render_template, request, redirect, url_for
import MySQLdb
import os
from werkzeug.utils import secure_filename

disease_recognition = Blueprint('crop_disease', __name__)

# Database Connection
db = MySQLdb.connect(host="localhost", user="root", passwd="", db="crop_yield_db")
cursor = db.cursor()

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'static/uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@disease_recognition.route('/crop-disease', methods=['GET', 'POST'])
def crop_disease():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('crop_disease.html', error="No file uploaded.")
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return render_template('crop_disease.html', error="Invalid file type.")
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Extract crop name from filename (Assuming filename contains crop name)
        crop_name = filename.rsplit('.', 1)[0].lower()
        
        # Fetch disease details from database
        cursor.execute("SELECT disease_name, prevention_measures, expected_yield FROM crop_diseases WHERE crop_name = %s", (crop_name,))
        results = cursor.fetchall()
        
        if results:
            diseases = [dict(disease_name=row[0], prevention_measures=row[1], expected_yield=row[2]) for row in results]
        else:
            diseases = [{"disease_name": "Unknown", "prevention_measures": "No data available", "expected_yield": "No data available"}]
        
        return render_template('crop_disease.html', filename=filename, crop_name=crop_name, diseases=diseases)
    
    return render_template('crop_disease.html')
