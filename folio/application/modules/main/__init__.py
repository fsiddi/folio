from flask import render_template
from application import app

from application.modules.main.model_user_settings import Setting
from application.modules.main.model_user_settings import SocialLink
from application.modules.main.model_projects import Category
from application.modules.main.model_projects import Project
from application.modules.pages import view
from application.modules.theme import get_theme_dir

from sqlalchemy import desc


###### Data to be injected for use in the templates

@app.context_processor
def inject_settings():
    settings = Setting.query.all()
    settings_dic = {}
    for setting in settings:
        settings_dic[setting.name] = setting.value
    return settings_dic


@app.context_processor
def inject_categories():
    categories = Category.query.all()
    categories_list = [(category.url, category.name) for category in categories]
    return {'categories' : categories_list}


@app.context_processor
def inject_social_links():
    links = SocialLink.query.order_by(SocialLink.order).all()
    links_list = [(l.icon, l.handle, l.href) for l in links]
    return {'social_links' : links_list}



###### Routes

@app.route('/')
def homepage():
    return index_projects(Category.query.first_or_404().url)

@app.route('/about')
def about():
    return view('about')


@app.route('/<category>')
def index_projects(category):
    if Category.query.filter_by(url=category).first_or_404():
        projects = Project.query.join(Category).\
            filter(Category.url == category).\
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
        get_theme_dir() + '/project.html',
        project=project,
        title=category)


import contact




######  Custom error handling

@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        get_theme_dir() + 'error.html', code="404", desc="Page not Found"), 404

@app.errorhandler(403)
def forbidden(error):
    return render_template(
        get_theme_dir() + 'error.html', code="403", desc="Forbidden"), 403

@app.errorhandler(401)
def not_authorized(error):
    return render_template(
        get_theme_dir() + 'error.html', code="401", desc="Not Authorized"), 401

