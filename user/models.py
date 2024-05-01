from flask_pymongo import PyMongo
from flask import Flask, jsonify, request, session, redirect
#from bson.objectid import ObjectId
import uuid
import bcrypt
from extensions import mongo


class User:
    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        print(session)
        return jsonify(user), 200

    def sign_up(self):
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
            from app import start_session
            return start_session(user_data)
        return jsonify({ "error": "Signup failed" }), 400
    
    def signout(self):
        session.clear()
        return jsonify({"message": "signed out"}), 200
    
    def update_user(self):
        print(session)
        data = request.json
        if 'logged_in' in session:
            print(234)
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
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        user = self.find_by_email(email)

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return self.start_session(user)
        
        return jsonify({ "error": "Invalid login credentials" }), 401

    #@staticmethod
    #def find_by_id(user_id):
        #return mongo.db.users.find_one({"_id": ObjectId(user_id)})
    @staticmethod
    def find_by_username(username):
        return mongo.db.users.find_one({"username": username})

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})
    
