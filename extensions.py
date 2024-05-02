from flask_pymongo import PyMongo
from flask import Flask
from datetime import timedelta

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mixmatch'


app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.secret_key = b'\x07\x19\x98\x01\xd5\x1dy\xc5\x8a\x14p\xa4\xe6*`\xbc'

mongo = PyMongo(app)
