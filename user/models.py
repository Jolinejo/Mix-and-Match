from flask import jsonify, request, session
import uuid
import bcrypt
from extensions import mongo


class User:
    """User class with user funcitons for the routes"""

    def start_session(self, user):
        """starts a session and removes the password"""
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        print(session)
        return jsonify(user), 200

    def sign_up(self):
        """signs up a user and starts the session"""
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        if not username or not email or not password:
            return jsonify({'error': 'Missing required fields'}), 400

        if self.find_by_username(username):
            return jsonify({'error': 'Username already exists'}), 400

        if self.find_by_email(email):
            return jsonify({'error': 'Email already exists'}), 400
        user_data = {
            "_id": uuid.uuid4().hex,
            "username": username,
            "email": email,
            "password": hashed_password
        }
        if mongo.db.users.insert_one(user_data):
            return self.start_session(user_data)
        return jsonify({ "error": "Signup failed" }), 400
    
    def signout(self):
        """clears the session to sign out the user"""
        session.clear()
        return jsonify({"message": "signed out"}), 200
    
    def update_user(self):
        """updates the user based on sent keys and values"""
        data = request.json
        user_id = session['user']['_id']

        user = mongo.db.users.find_one({"_id": user_id})

        if not user:
            return jsonify({"error": "User not found"}), 404

        for key, value in data.items():
            user[key] = value
        
        result = mongo.db.users.update_one({"_id": user_id}, {"$set": user})

        if result.modified_count == 1:
            return jsonify({"message": "User updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to update user"}), 500
    
    def get_user_data(self):
        """retrieves user data based on query keys"""
        keys = request.args.getlist('keys')
        if 'user' not in session:
            return jsonify({"error": "User not logged in"}), 401

        user_id = session['user']['_id']

        user = mongo.db.users.find_one({"_id": user_id})

        if not user:
            return jsonify({"error": "User not found"}), 404

        user_data = {key: user.get(key) for key in keys}

        return jsonify(user_data), 200
    
    def login(self):
        """logs in user and starts the session"""
        data = request.json
        email = data.get('email')
        password = data.get('password')

        user = self.find_by_email(email)

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return self.start_session(user)
        
        return jsonify({ "error": "Invalid login credentials" }), 401


    @staticmethod
    def find_by_username(username):
        return mongo.db.users.find_one({"username": username})

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})
    