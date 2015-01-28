from flask import render_template

from application import app
from application import db

from application.modules.projects.model import Category
from application.modules.projects.model import Project
from application.modules.theme import get_theme_dir

from flask import render_template

from sqlalchemy import desc


@app.route('/')
def homepage():
    return index_projects('film')


@app.route('/<category>')
def index_projects(category):
    if Category.query.filter_by(url=category).first_or_404():
        projects = Project.query.join(Category).\
            filter(Category.name == category).\
            order_by(desc(Project.creation_date)).\
            all()
        return render_template(
            get_theme_dir() + '/projects.html',
            title=category,
            projects=projects)


@app.route('/<category>/<project>')
def project(category, project):
    project = Project.query.join(Category).\
        filter(Category.url == category).\
        filter(Project.url == project).\
        first_or_404()
    return render_template(
        get_theme_dir() + '/project.html', project=project)

