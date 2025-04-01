from flask import Blueprint, render_template, request
import mysql.connector

market_bp = Blueprint('market', __name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="crop_yield_db"
    )

@market_bp.route('/market-prices', methods=['GET', 'POST'])
def market_prices():
    product_name = request.form.get('product_name') if request.method == 'POST' else ''
    data = []

    if product_name:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM market_prices WHERE product_name LIKE %s"
        cursor.execute(query, (f"%{product_name}%",))
        data = cursor.fetchall()
        cursor.close()
        conn.close()

    return render_template('market_prices.html', data=data, product_name=product_name)
