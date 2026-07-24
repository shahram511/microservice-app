import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import jwt

app = Flask(__name__)
CORS(app)

# 1. Reading the credentials from the container's environment variables
db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASS')
db_host = os.environ.get('DB_HOST')

# === NEW ADDITION: Read the secret key injected by Docker ===
SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

if not SECRET_KEY:
    raise ValueError("No JWT_SECRET_KEY set for Flask application. Check docker-compose.yml")
# ============================================================

# 2. Constructing the connection string with the 'admin' authSource
mongo_uri = f"mongodb://{db_user}:{db_pass}@{db_host}:27017/?authSource=admin"

# 3. Initializing the MongoDB client with the secure URI
client = MongoClient(mongo_uri)
db = client['user_database']
users_collection = db['users']

@app.route('/api/users', methods=['POST'])
def add_user():
    auth_header = request.headers.get('Authorization')
        
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Unauthorized: Missing or invalid token format"}), 401
        
    # Extract the actual token from "Bearer <token>" (Indentation fixed here)
    token = auth_header.split(" ")[1]
        
    try:
        # Mathematically verify the token signature and expiration
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print(f"Authenticated request from: {decoded_payload.get('email')}")
        
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Unauthorized: Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Unauthorized: Invalid token signature"}), 401

    # Extract JSON data from the request
    data = request.get_json()
    
    # Check if data was successfully parsed as JSON
    if not data:
        return jsonify({'error': 'Invalid JSON format or empty data!'}), 400
        
    name = data.get('name')
    email = data.get('email')
    
    # Validate that both fields exist
    if name and email:
        user_data = {
            'name': name,
            'email': email
        }
        
        # Insert the document into MongoDB
        users_collection.insert_one(user_data)
        
        return jsonify({'message': 'User added successfully'}), 201
        
    return jsonify({'error': 'Incomplete form data!'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)