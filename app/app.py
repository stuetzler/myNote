from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
# from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate

from flask_restful import Api
from api import apiAuth

from main import main 
from auth import auth 
from db import db 
from models import User

app = Flask(__name__)
# api = Api(app)
# auth = HTTPBasicAuth()

# Configure the app
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://flask_app_user:flask_app_password@mysql:3306/flask_app_db'

# Create the database
db.init_app(app)

# Setup LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# Initialize Flask-Migrate with the app and db
migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(auth,url_prefix="")
app.register_blueprint(main,url_prefix="")
app.register_blueprint(apiAuth,url_prefix="")

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)