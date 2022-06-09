from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Bundle, Environment
from werkzeug.security import generate_password_hash
from flask_login import LoginManager
import os
from os import environ
import secrets 
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
# ToDo Modify key for production
app.secret_key = secrets.token_hex() # secret key to enable sessions
app.config['SECRET_KEY'] = 'SECRET_KEY'
# bundle CSS
css = Bundle('src/style.css', output='css/main.css', filters='postcss')

assets = Environment(app)
assets.register('main_css', css)
css.build()

#path = os.path.join(os.path.dirname(__file__), 'web.db') # to ensure that works on any machine (with any folder setup)
 

# uses SQLite in development but Postgres in production for Heroku
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ------- Managing logged in state -------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # The name of the view to redirect to when the user needs to log in. 
