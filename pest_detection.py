from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
import os
from flask_mysqldb import MySQL

# Blueprint for pest detection
pest_detection_bp = Blueprint('pest_detection', __name__)

# MySQL connection (Ensure it's initialized in `app.py`)
mysql = MySQL()

# Upload folder for images
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Pest Detection Route
@pest_detection_bp.route('/pest-detection', methods=['GET', 'POST'])
def pest_detection():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('pest_detection.html', error='No file uploaded.')

        file = request.files['file']
        if file.filename == '':
            return render_template('pest_detection.html', error='No selected file.')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Check if image name exists in MySQL
            cur = mysql.connection.cursor()
            cur.execute("SELECT disease_name, cause, effects, solution FROM pest_diseases WHERE image_name = %s", (filename,))
            disease_info = cur.fetchone()
            cur.close()

            if disease_info:
                return render_template('pest_detection.html', filename=filename, disease_info=disease_info)
            else:
                return render_template('pest_detection.html', filename=filename, error='No matching disease found in database.')

    return render_template('pest_detection.html')
