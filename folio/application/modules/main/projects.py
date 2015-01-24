from flask import (abort,
                   Blueprint,
                   jsonify,
                   render_template,
                   redirect,
                   request,
                   url_for)

from application import app
from application import db

from application.models.model import (
    Project,
    Category,
    Setting)

from sqlalchemy import desc
from flask.ext.login import login_user

from application.modules.theme import get_theme_dir



@app.context_processor
def inject_settings():
    settings = Setting.query.all()
    settings_dic = {}
    for setting in settings:
        settings_dic[setting.name] = setting.value
    return settings_dic

@app.route('/')
def homepage():
    return index_projects('film')



@app.route('/<category>')
def index_projects(category):
    if Category.query.filter_by(name=category).first_or_404():
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
        filter(Category.name == category).\
        filter(Project.url == project).\
        first_or_404()
    return render_template(
        get_theme_dir() + '/project.html', project=project)

