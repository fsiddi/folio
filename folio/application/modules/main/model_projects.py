from application import app
from application import db

import datetime

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(120), nullable=False)

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


class Picture(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    alt = db.Column(db.String(120), nullable=False)
    path = db.Column(db.String(120), nullable=False)

    project_id = db.Column(db.Integer(), db.ForeignKey(Project.id))
    project = db.relationship(Project, backref='Gallery')
