# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, logout_user, current_user
import sqlite3
from flask_login import UserMixin
app = Flask(__name__)
app.config["SECRET_KEY"]="kkk"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

#after initializing flask
from routes import *


if __name__ =="__main__":
    app.run(debug=True)

