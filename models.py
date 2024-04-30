from flask_pymongo import PyMongo
#from bson.objectid import ObjectId
import app
import uuid

from app import mongo

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def save_to_db(self):
        user_data = {
            "_id": uuid.uuid4().hex,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
        mongo.db.users.insert_one(user_data)

    @staticmethod
    def find_by_username(username):
        return mongo.db.users.find_one({"username": username})

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})

    #@staticmethod
    #def find_by_id(user_id):
        #return mongo.db.users.find_one({"_id": ObjectId(user_id)})
