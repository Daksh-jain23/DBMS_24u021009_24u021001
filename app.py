from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

def get_db_config():
    return {
        'host': 'localhost',
        'user': 'root',
        'password': 'D@ksh@SQL',
        'database': 'dbms_proj',
    }

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**get_db_config())
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def execute_query(query, params=None, fetch=False):
    """Execute a database query and return results if fetch=True"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
        else:
            connection.commit()
            result = cursor.lastrowid
        return result
    except Error as e:
        # Let callers handle and report proper errors
        raise e
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Map DB errors to friendly API responses
def handle_db_error(e):
    code = getattr(e, "errno", None)
    raw = str(e)
    status = 400
    message = "Invalid data. Please check your input."

    if code == 1062:
        # Duplicate entry (UNIQUE constraint)
        status = 409
        message = "Duplicate value violates a UNIQUE constraint."
    elif code == 1048:
        # Column cannot be null
        message = "A required field is missing."
    elif code == 1452:
        # Foreign key constraint fails
        message = "Foreign key constraint failed. Ensure referenced records exist."
    elif code == 3819:
        # Check constraint
        message = "A CHECK constraint failed. Please correct your input values."

    return jsonify({"message": message, "details": raw, "code": code}), status

# Routes for serving HTML pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/farmers')
def farmers():
    return render_template('farmers.html')

@app.route('/crops')
def crops():
    return render_template('crops.html')

@app.route('/markets')
def markets():
    return render_template('markets.html')

@app.route('/transactions')
def transactions():
    return render_template('transactions.html')

@app.route('/api/farmers', methods=['GET'])
def get_farmers():
    query = "SELECT * FROM Farmers ORDER BY farmer_id"
    try:
        farmers = execute_query(query, fetch=True)
        return jsonify(farmers)
    except Error as e:
        return handle_db_error(e)

@app.route('/api/farmers', methods=['POST'])
def create_farmer():
    try:
        data = request.get_json()
        query = "INSERT INTO Farmers (farmer_name, village, phone) VALUES (%s, %s, %s)"
        params = (data.get('farmer_name'), data.get('village'), data.get('phone'))
        farmer_id = execute_query(query, params)
        return jsonify({'message': 'Farmer created successfully', 'farmer_id': farmer_id})
    except Error as e:
        return handle_db_error(e)

@app.route('/api/farmers/<int:farmer_id>', methods=['PUT'])
def update_farmer(farmer_id):
    try:
        data = request.get_json()
        query = "UPDATE Farmers SET farmer_name=%s, village=%s, phone=%s WHERE farmer_id=%s"
        params = (data.get('farmer_name'), data.get('village'), data.get('phone'), farmer_id)
        execute_query(query, params)
        return jsonify({'message': 'Farmer updated successfully'})
    except Error as e:
        return handle_db_error(e)

@app.route('/api/farmers/<int:farmer_id>', methods=['DELETE'])
def delete_farmer(farmer_id):
    try:
        query = "DELETE FROM Farmers WHERE farmer_id=%s"
        execute_query(query, (farmer_id,))
        return jsonify({'message': 'Farmer deleted successfully'})
    except Error as e:
        return handle_db_error(e)

# Crops API endpoints
@app.route('/api/crops', methods=['GET'])
def get_crops():
    query = "SELECT * FROM Crops ORDER BY crop_id"
    try:
        crops = execute_query(query, fetch=True)
        return jsonify(crops)
    except Error as e:
        return handle_db_error(e)

@app.route('/api/crops', methods=['POST'])
def create_crop():
    try:
        data = request.get_json()
        query = "INSERT INTO Crops (crop_name, season) VALUES (%s, %s)"
        params = (data.get('crop_name'), data.get('season'))
        crop_id = execute_query(query, params)
        return jsonify({'message': 'Crop created successfully', 'crop_id': crop_id})
    except Error as e:
        return handle_db_error(e)

@app.route('/api/crops/<int:crop_id>', methods=['PUT'])
def update_crop(crop_id):
    try:
        data = request.get_json()
        query = "UPDATE Crops SET crop_name=%s, season=%s WHERE crop_id=%s"
        params = (data.get('crop_name'), data.get('season'), crop_id)
        execute_query(query, params)
        return jsonify({'message': 'Crop updated successfully'})
    except Error as e:
        return handle_db_error(e)

@app.route('/api/crops/<int:crop_id>', methods=['DELETE'])
def delete_crop(crop_id):
    try:
        query = "DELETE FROM Crops WHERE crop_id=%s"
        execute_query(query, (crop_id,))
        return jsonify({'message': 'Crop deleted successfully'})
    except Error as e:
        return handle_db_error(e)

# Markets API endpoints
@app.route('/api/markets', methods=['GET'])
def get_markets():
    query = "SELECT * FROM Markets ORDER BY market_id"
    try:
        markets = execute_query(query, fetch=True)
        return jsonify(markets)
    except Error as e:
        return handle_db_error(e)

@app.route('/api/markets', methods=['POST'])
def create_market():
    try:
        data = request.get_json()
        query = "INSERT INTO Markets (market_name, location) VALUES (%s, %s)"
        params = (data.get('market_name'), data.get('location'))
        market_id = execute_query(query, params)
        return jsonify({'message': 'Market created successfully', 'market_id': market_id})
    except Error as e:
        return handle_db_error(e)

@app.route('/api/markets/<int:market_id>', methods=['PUT'])
def update_market(market_id):
    try:
        data = request.get_json()
        query = "UPDATE Markets SET market_name=%s, location=%s WHERE market_id=%s"
        params = (data.get('market_name'), data.get('location'), market_id)
        execute_query(query, params)
        return jsonify({'message': 'Market updated successfully'})
    except Error as e:
        return handle_db_error(e)

@app.route('/api/markets/<int:market_id>', methods=['DELETE'])
def delete_market(market_id):
    try:
        query = "DELETE FROM Markets WHERE market_id=%s"
        execute_query(query, (market_id,))
        return jsonify({'message': 'Market deleted successfully'})
    except Error as e:
        return handle_db_error(e)

# Transactions API endpoints
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    query = """
    SELECT t.*, f.farmer_name, c.crop_name, m.market_name 
    FROM Transactions t
    LEFT JOIN Farmers f ON t.farmer_id = f.farmer_id
    LEFT JOIN Crops c ON t.crop_id = c.crop_id
    LEFT JOIN Markets m ON t.market_id = m.market_id
    ORDER BY t.transaction_id
    """
    try:
        transactions = execute_query(query, fetch=True)
        return jsonify(transactions)
    except Error as e:
        return handle_db_error(e)

@app.route('/api/transactions', methods=['POST'])
def create_transaction():
    try:
        data = request.get_json()
        query = "INSERT INTO Transactions (farmer_id, crop_id, market_id, quantity, price) VALUES (%s, %s, %s, %s, %s)"
        params = (data.get('farmer_id'), data.get('crop_id'), data.get('market_id'), data.get('quantity'), data.get('price'))
        transaction_id = execute_query(query, params)
        return jsonify({'message': 'Transaction created successfully', 'transaction_id': transaction_id})
    except Error as e:
        return handle_db_error(e)

@app.route('/api/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    try:
        data = request.get_json()
        query = "UPDATE Transactions SET farmer_id=%s, crop_id=%s, market_id=%s, quantity=%s, price=%s WHERE transaction_id=%s"
        params = (data.get('farmer_id'), data.get('crop_id'), data.get('market_id'), data.get('quantity'), data.get('price'), transaction_id)
        execute_query(query, params)
        return jsonify({'message': 'Transaction updated successfully'})
    except Error as e:
        return handle_db_error(e)

@app.route('/api/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    try:
        query = "DELETE FROM Transactions WHERE transaction_id=%s"
        execute_query(query, (transaction_id,))
        return jsonify({'message': 'Transaction deleted successfully'})
    except Error as e:
        return handle_db_error(e)

# API endpoint to get all data for dropdowns
@app.route('/api/farmers-list', methods=['GET'])
def get_farmers_list():
    query = "SELECT farmer_id, farmer_name FROM Farmers ORDER BY farmer_name"
    try:
        farmers = execute_query(query, fetch=True)
        return jsonify(farmers)
    except Error as e:
        return handle_db_error(e)

@app.route('/api/crops-list', methods=['GET'])
def get_crops_list():
    query = "SELECT crop_id, crop_name FROM Crops ORDER BY crop_name"
    try:
        crops = execute_query(query, fetch=True)
        return jsonify(crops)
    except Error as e:
        return handle_db_error(e)

@app.route('/api/markets-list', methods=['GET'])
def get_markets_list():
    query = "SELECT market_id, market_name FROM Markets ORDER BY market_name"
    try:
        markets = execute_query(query, fetch=True)
        return jsonify(markets)
    except Error as e:
        return handle_db_error(e)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)




