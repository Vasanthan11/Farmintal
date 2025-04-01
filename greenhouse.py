from flask import Blueprint, render_template
import MySQLdb

greenhouse = Blueprint('greenhouse', __name__)

# Connect to MySQL
db = MySQLdb.connect(host="localhost", user="root", passwd="", db="crop_yield_db")
cursor = db.cursor()

@greenhouse.route('/greenhouse-control')
def greenhouse_control():
    cursor.execute("""
        SELECT timestamp, temperature, humidity, soil_moisture, co2_level, light_intensity, ph_level 
        FROM greenhouse_data ORDER BY timestamp DESC LIMIT 10
    """)
    data = cursor.fetchall()

    if not data:
        return render_template('greenhouse.html', alert="No data available!", 
                               temperature=0, humidity=0, soil_moisture=0, 
                               co2_level=0, light_intensity=0, ph_level=0,
                               timestamps=[], temperature_data=[], humidity_data=[], 
                               soil_moisture_data=[], co2_data=[], light_data=[], ph_data=[])

    timestamps = [row[0].strftime('%H:%M') for row in data]
    temperature_data = [row[1] for row in data]
    humidity_data = [row[2] for row in data]
    soil_moisture_data = [row[3] for row in data]
    co2_data = [row[4] if row[4] is not None else 0 for row in data]  # Avoid None values
    light_data = [row[5] if row[5] is not None else 0 for row in data]
    ph_data = [row[6] if row[6] is not None else 7 for row in data]  # Default to neutral pH

    # Get the latest values
    latest_temp, latest_humidity, latest_moisture, latest_co2, latest_light, latest_ph = data[0][1:7]

    # Alerts based on values
    alert = None
    if latest_temp > 35:
        alert = "🔥 High Temperature Alert!"
    elif latest_temp < 15:
        alert = "❄️ Low Temperature Alert!"
    if latest_humidity < 30:
        alert = "🔴 Low Humidity Warning!"
    elif latest_humidity > 80:
        alert = "🔵 High Humidity Alert!"
    if latest_moisture < 20:
        alert = "🏜️ Soil is too dry, needs irrigation!"
    elif latest_moisture > 80:
        alert = "🌊 Soil is overwatered!"
    if latest_co2 > 1000:
        alert = "🚨 High CO₂ Level Warning!"
    elif latest_co2 < 300:
        alert = "⚠️ Low CO₂ Level Alert!"
    if latest_ph < 5.5:
        alert = "⚠️ Soil is too acidic!"
    elif latest_ph > 7.5:
        alert = "⚠️ Soil is too alkaline!"

    return render_template('greenhouse.html', 
                           temperature=latest_temp, humidity=latest_humidity, soil_moisture=latest_moisture, 
                           co2_level=latest_co2, light_intensity=latest_light, ph_level=latest_ph,
                           timestamps=timestamps, temperature_data=temperature_data, 
                           humidity_data=humidity_data, soil_moisture_data=soil_moisture_data,
                           co2_data=co2_data, light_data=light_data, ph_data=ph_data,
                           alert=alert)
