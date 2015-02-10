from flask import Flask, Blueprint
from flask.ext.mail import Mail
from flask.ext.cache import Cache
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.thumbnails import Thumbnail
from flask.ext.login import LoginManager, UserMixin


# Initialize the Flask all object
app = Flask(__name__)

# Choose the configuration to load
import config
app.config.from_object(config.Development)


# Create database connection object
db = SQLAlchemy(app)
# Set up email
mail = Mail(app)
# Set up caching
cache = Cache(app)
# Thumbnails
thumb = Thumbnail(app)
# Flask-Login
login_manager = LoginManager(app)
# create user loader function
@login_manager.user_loader
def load_user(username):
    return main.model_user_settings.User.get(username)


# Import all modules
from modules import main
from modules import admin
from modules import pages


# Register blueprints for the imported controllers
filemanager = Blueprint('filemanager', __name__, static_folder='static/files')
app.register_blueprint(filemanager)
# app.register_blueprint(shots, url_prefix='/shots')
# app.register_blueprint(projects, url_prefix='/projects')
