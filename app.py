from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


from flask import Flask
from pest_detection import pest_detection_bp
from flask_mysqldb import MySQL



nav_items = [
    {'name': 'Home', 'url': '/', 'icon': 'fas fa-home'},
    {'name': 'Crop Yield Prediction', 'url': '/crop-yield', 'icon': 'fas fa-seedling'},
    {'name': 'Weather Data Analysis', 'url': '/weather-analysis', 'icon': 'fas fa-cloud-sun'},
    {'name': 'Soil Quality Checker', 'url': '/soil-analysis', 'icon': 'fas fa-mountain'},
    {'name': 'Pest Detection System', 'url': '/pest-detection', 'icon': 'fas fa-bug'},
    {'name': 'Irrigation Controller', 'url': '/irrigation', 'icon': 'fas fa-water'},
    {'name': 'Crop Disease Recognition', 'url': '/crop-disease', 'icon': 'fas fa-virus'},
    {'name': 'Crop Rotation Planner', 'url': '/crop-rotation', 'icon': 'fas fa-sync-alt'},
    {'name': 'Farm Market Price Tracker', 'url': '/market-prices', 'icon': 'fas fa-chart-line'},
    {'name': 'Farm Inventory Tracker', 'url': '/inventory', 'icon': 'fas fa-warehouse'},
    {'name': 'Automated Greenhouse Control', 'url': '/greenhouse-control', 'icon': 'fas fa-leaf'},
    {'name': 'Crop Storage Management', 'url': '/crop-storage', 'icon': 'fas fa-box'}
]
app = Flask(__name__)
app.secret_key = "your_secret_key" 

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crop_yield_db'

mysql = MySQL(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# User Model
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(user[0], user[1])
    return None

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']   
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        if user and bcrypt.check_password_hash(user[2], password):
            login_user(User(user[0], user[1]))
            return redirect(url_for('nav'))  # Redirect to Navigation Page
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/nav')
@login_required
def nav():
    return render_template('nav.html', nav_items=nav_items)

@app.route('/soil-analysis', methods=['GET', 'POST'])
@login_required
def soil_analysis():
    if request.method == 'POST':
        nitrogen = float(request.form['nitrogen'])
        phosphorus = float(request.form['phosphorus'])
        potassium = float(request.form['potassium'])
        pH = float(request.form['pH'])
        organic_matter = float(request.form['organic_matter'])

        # Fetch matching crops from database
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT crop_name FROM soil_data 
            WHERE nitrogen <= %s + 10 AND nitrogen >= %s - 10
            AND phosphorus <= %s + 10 AND phosphorus >= %s - 10
            AND potassium <= %s + 10 AND potassium >= %s - 10
            AND pH BETWEEN %s - 0.5 AND %s + 0.5
            ORDER BY organic_matter DESC LIMIT 3
        """, (nitrogen, nitrogen, phosphorus, phosphorus, potassium, potassium, pH, pH))

        crops = cur.fetchall()
        cur.close()

        if crops:
            crop_list = [crop[0] for crop in crops]  # Extract crop names
            return render_template('soil_analysis.html', recommended_crops=crop_list)
        else:
            return render_template('soil_analysis.html', recommended_crops=["No suitable crop found"])

    return render_template('soil_analysis.html')


@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    if request.method == 'POST':
        temp = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        rainfall = float(request.form['rainfall'])

        # Dummy dataset for training (Replace with real data)
        data = {
            'temperature': [25, 30, 35, 40, 45],
            'humidity': [50, 55, 60, 65, 70],
            'rainfall': [100, 120, 140, 160, 180],
            'crop_yield': [2.5, 3.0, 3.5, 4.0, 4.5]
        }
        df = pd.DataFrame(data)

        # Train Model
        X = df[['temperature', 'humidity', 'rainfall']]
        y = df['crop_yield']
        model = LinearRegression()
        model.fit(X, y)

        # Predict
        prediction = model.predict([[temp, humidity, rainfall]])[0]

        return render_template('predict.html', prediction=round(prediction, 2))
    return render_template('predict.html')



@app.route('/crop-yield', methods=['GET', 'POST'])
@login_required
def crop_yield():
    if request.method == 'POST':
        temp = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        rainfall = float(request.form['rainfall'])

        # Dummy dataset for training (Replace with real data later)
        data = {
            'temperature': [25, 30, 35, 40, 45],
            'humidity': [50, 55, 60, 65, 70],
            'rainfall': [100, 120, 140, 160, 180],
            'crop_yield': [2.5, 3.0, 3.5, 4.0, 4.5]
        }
        df = pd.DataFrame(data)

        X = df[['temperature', 'humidity', 'rainfall']]
        y = df['crop_yield']
        model = LinearRegression()
        model.fit(X, y)

        predicted_yield = model.predict([[temp, humidity, rainfall]])[0]

        return render_template('crop_yield.html', prediction=round(predicted_yield, 2))
    return render_template('crop_yield.html')




@app.route('/weather-analysis')
def weather_analysis():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM weather_data")
    data = cursor.fetchall()

    # Convert to dictionary so Jinja2 can access columns by name
    weather_data = []
    for row in data:
        weather_data.append({
            'date': row[1],
            'temperature': row[2],
            'humidity': row[3],
            'rainfall': row[4]
        })
        

    # Average calculations
    cursor.execute("SELECT AVG(temperature), AVG(humidity), AVG(rainfall) FROM weather_data")
    avg_temp, avg_hum, avg_rain = cursor.fetchone()

    if avg_temp < 25 and avg_rain > 100:
        crop = "Rice, Jute"
    elif 25 <= avg_temp <= 30 and avg_rain < 100:
        crop = "Wheat, Barley, Maize"
    elif avg_temp > 30:
        crop = "Millets, Cotton, Sorghum"
    else:
        crop = "Vegetables or Legumes"

    return render_template("weather_analysis.html", weather_data=weather_data, recommended_crop=crop)


# Register the pest detection blueprint
app.register_blueprint(pest_detection_bp)


from greenhouse import greenhouse  # Import Greenhouse Blueprint
app.register_blueprint(greenhouse)


from crop_disease import disease_recognition
app.register_blueprint(disease_recognition)


from market import market_bp
app.register_blueprint(market_bp)


from crop_storage import crop_storage_bp
app.register_blueprint(crop_storage_bp)


from crop_rotation import crop_rotation_bp
app.register_blueprint(crop_rotation_bp)


from irrigation import irrigation_bp
app.register_blueprint(irrigation_bp)








# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)


if __name__ == '__main__':
    app.run(debug=True)
