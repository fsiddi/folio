from application import app
from application import db

import os
import os.path as op
import datetime

import hashlib
import time

from werkzeug import secure_filename
from sqlalchemy import event
from sqlalchemy.event import listens_for

from flask import (
    render_template, 
    jsonify, 
    redirect, 
    url_for, 
    request)

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin


def prefix_name(obj, file_data):
    # Collect name and extension
    parts = op.splitext(file_data.filename)
    # Get current time (for unique hash)
    timestamp = str(round(time.time()))
    # Has filename only (not extension)
    file_name = secure_filename(timestamp + '%s' % parts[0])
    # Put them together
    full_name = hashlib.md5(file_name).hexdigest() + parts[1]
    return full_name


# Create directory for file fields to use
file_path = op.join(op.dirname(__file__), 'static/files',)
try:
    os.mkdir(file_path)
except OSError:
    pass


class User(UserMixin):
    """
    User Class for flask-Login. This is not stored in the database. This
    can be improved further http://thecircuitnerd.com/flask-login-tokens/"""
    def __init__(self, userid, password):
        self.id = userid
        self.password = password
  
    @staticmethod
    def get(userid):
        """
        Static method to search the database and see if userid exists.  If it 
        does exist then return a User Object.  If not then return None as 
        required by Flask-Login."""
        
        # We get the username and password from a static list stored in the 
        # preferences. This can be probably a bit smarter, but for a single
        # user system it does not require a whole database table
        try:
            password = app.config['USERS'][userid]
            return User(userid, password)
        except KeyError:
            return None


class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable=False)

    def __str__(self):
        return self.name


class Project(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    picture = db.Column(db.String(120))
    video = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook = db.Column(db.String(120))
    creation_date = db.Column(db.DateTime(), default=datetime.datetime.now)

    category_id = db.Column(db.Integer(), db.ForeignKey(Category.id))
    category = db.relationship(Category, backref='Project')

    def __str__(self):
        return self.name


class Setting(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable=False)
    value = db.Column(db.String(256), nullable=False)

    def __str__(self):
        return str(self.value)


class Picture(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    alt = db.Column(db.String(120), nullable=False)
    path = db.Column(db.String(120), nullable=False)

    project_id = db.Column(db.Integer(), db.ForeignKey(Project.id))
    project = db.relationship(Project, backref='Gallery')
