from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import bcrypt
app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/mixmatch'

mongo = PyMongo(app)

@app.route('/')
def index():
    cursor = mongo.db.users.find({})  # Retrieve data from MongoDB
    usernames = [doc['username'] for doc in cursor]  # Extract usernames from documents

    return jsonify(usernames)

@app.route('/register', methods=['POST'])
def register():
    """Registers a new user"""
    request_data = request.get_json()
    username = request_data.get('username')
    email = request_data.get('email')
    password = request_data.get('password')

    # Check if username or email already exists
    existing_user = mongo.db.users.find_one({'$or': [{'username': username}, {'email': email}]})

    if existing_user:
        return jsonify({'message': 'Username or email already exists'}), 400

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert the new user into the database
    new_user = {
        'username': username,
        'email': email,
        'password': hashed_password
    }
    mongo.db.users.insert_one(new_user)

    return jsonify({'message': 'User registered successfully'}), 201


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5001)