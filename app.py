import os
from urllib.parse import urlparse
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

def get_db_config():
    """Get database configuration from DATABASE_URL or fallback to local MySQL"""
    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        url = urlparse(database_url)
        return {
            'host': url.hostname,
            'user': url.username,
            'password': url.password,
            'database': url.path.lstrip('/'),
            'port': url.port or 3306
        }
    else:
        # Fallback for local testing
        return {
            'host': 'localhost',
            'user': 'root',
            'password': 'D@ksh@SQL',
            'database': 'dbms_proj'
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
        print(f"Error executing query: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

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
    farmers = execute_query(query, fetch=True)
    return jsonify(farmers)

@app.route('/api/farmers', methods=['POST'])
def create_farmer():
    data = request.get_json()
    query = "INSERT INTO Farmers (farmer_name, village, phone) VALUES (%s, %s, %s)"
    params = (data['farmer_name'], data.get('village'), data.get('phone'))
    farmer_id = execute_query(query, params)
    return jsonify({'message': 'Farmer created successfully', 'farmer_id': farmer_id})

@app.route('/api/farmers/<int:farmer_id>', methods=['PUT'])
def update_farmer(farmer_id):
    data = request.get_json()
    query = "UPDATE Farmers SET farmer_name=%s, village=%s, phone=%s WHERE farmer_id=%s"
    params = (data['farmer_name'], data.get('village'), data.get('phone'), farmer_id)
    execute_query(query, params)
    return jsonify({'message': 'Farmer updated successfully'})

@app.route('/api/farmers/<int:farmer_id>', methods=['DELETE'])
def delete_farmer(farmer_id):
    query = "DELETE FROM Farmers WHERE farmer_id=%s"
    execute_query(query, (farmer_id,))
    return jsonify({'message': 'Farmer deleted successfully'})

# Crops API endpoints
@app.route('/api/crops', methods=['GET'])
def get_crops():
    query = "SELECT * FROM Crops ORDER BY crop_id"
    crops = execute_query(query, fetch=True)
    return jsonify(crops)

@app.route('/api/crops', methods=['POST'])
def create_crop():
    data = request.get_json()
    query = "INSERT INTO Crops (crop_name, season) VALUES (%s, %s)"
    params = (data['crop_name'], data.get('season'))
    crop_id = execute_query(query, params)
    return jsonify({'message': 'Crop created successfully', 'crop_id': crop_id})

@app.route('/api/crops/<int:crop_id>', methods=['PUT'])
def update_crop(crop_id):
    data = request.get_json()
    query = "UPDATE Crops SET crop_name=%s, season=%s WHERE crop_id=%s"
    params = (data['crop_name'], data.get('season'), crop_id)
    execute_query(query, params)
    return jsonify({'message': 'Crop updated successfully'})

@app.route('/api/crops/<int:crop_id>', methods=['DELETE'])
def delete_crop(crop_id):
    query = "DELETE FROM Crops WHERE crop_id=%s"
    execute_query(query, (crop_id,))
    return jsonify({'message': 'Crop deleted successfully'})

# Markets API endpoints
@app.route('/api/markets', methods=['GET'])
def get_markets():
    query = "SELECT * FROM Markets ORDER BY market_id"
    markets = execute_query(query, fetch=True)
    return jsonify(markets)

@app.route('/api/markets', methods=['POST'])
def create_market():
    data = request.get_json()
    query = "INSERT INTO Markets (market_name, location) VALUES (%s, %s)"
    params = (data['market_name'], data.get('location'))
    market_id = execute_query(query, params)
    return jsonify({'message': 'Market created successfully', 'market_id': market_id})

@app.route('/api/markets/<int:market_id>', methods=['PUT'])
def update_market(market_id):
    data = request.get_json()
    query = "UPDATE Markets SET market_name=%s, location=%s WHERE market_id=%s"
    params = (data['market_name'], data.get('location'), market_id)
    execute_query(query, params)
    return jsonify({'message': 'Market updated successfully'})

@app.route('/api/markets/<int:market_id>', methods=['DELETE'])
def delete_market(market_id):
    query = "DELETE FROM Markets WHERE market_id=%s"
    execute_query(query, (market_id,))
    return jsonify({'message': 'Market deleted successfully'})

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
    transactions = execute_query(query, fetch=True)
    return jsonify(transactions)

@app.route('/api/transactions', methods=['POST'])
def create_transaction():
    data = request.get_json()
    query = "INSERT INTO Transactions (farmer_id, crop_id, market_id, quantity, price) VALUES (%s, %s, %s, %s, %s)"
    params = (data['farmer_id'], data['crop_id'], data['market_id'], data['quantity'], data['price'])
    transaction_id = execute_query(query, params)
    return jsonify({'message': 'Transaction created successfully', 'transaction_id': transaction_id})

@app.route('/api/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    data = request.get_json()
    query = "UPDATE Transactions SET farmer_id=%s, crop_id=%s, market_id=%s, quantity=%s, price=%s WHERE transaction_id=%s"
    params = (data['farmer_id'], data['crop_id'], data['market_id'], data['quantity'], data['price'], transaction_id)
    execute_query(query, params)
    return jsonify({'message': 'Transaction updated successfully'})

@app.route('/api/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    query = "DELETE FROM Transactions WHERE transaction_id=%s"
    execute_query(query, (transaction_id,))
    return jsonify({'message': 'Transaction deleted successfully'})

# API endpoint to get all data for dropdowns
@app.route('/api/farmers-list', methods=['GET'])
def get_farmers_list():
    query = "SELECT farmer_id, farmer_name FROM Farmers ORDER BY farmer_name"
    farmers = execute_query(query, fetch=True)
    return jsonify(farmers)

@app.route('/api/crops-list', methods=['GET'])
def get_crops_list():
    query = "SELECT crop_id, crop_name FROM Crops ORDER BY crop_name"
    crops = execute_query(query, fetch=True)
    return jsonify(crops)

@app.route('/api/markets-list', methods=['GET'])
def get_markets_list():
    query = "SELECT market_id, market_name FROM Markets ORDER BY market_name"
    markets = execute_query(query, fetch=True)
    return jsonify(markets)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


