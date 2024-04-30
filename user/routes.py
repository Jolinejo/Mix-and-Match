from flask import Flask, Blueprint
from user.models import User
from extensions import app
user_routes = Blueprint('user_routes', __name__)

user = User()
@user_routes.route('/user/register', methods=['POST'])
def register():
    return user.sign_up()

@user_routes.route('/user/login', methods=['POST'])
def login():
    return user.login()

@user_routes.route('/user/update', methods=['PUT'])
def update_user():
    return user.update_user()

@user_routes.route('/user/data', methods=['GET'])
def get_user_data():
    return user.get_user_data()

@user_routes.route('/user/signout')
def signout():
    return user.sign_up()