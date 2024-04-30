from flask import Flask, Blueprint
from user.models import User
from extensions import app
user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/user/register', methods=['POST'])
def register():
    print("H")
    return User().sign_up()

#@app.route('/user/signout')
#def signout():
    #from models import User
    #return User().sign_up()
