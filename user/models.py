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
            return self.start_session(user_data)
        return jsonify({ "error": "Signup failed" }), 400
    

    @staticmethod
    def find_by_username(username):
        return mongo.db.users.find_one({"username": username})

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})
    
    #def signout(self):
        #session.clear()
        #return redirect('/')

    #@staticmethod
    #def find_by_id(user_id):
        #return mongo.db.users.find_one({"_id": ObjectId(user_id)})
