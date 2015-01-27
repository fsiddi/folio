from flask import render_template
from application import app

from application.modules.main.model import Setting
from application.modules.theme import get_theme_dir


@app.context_processor
def inject_settings():
    settings = Setting.query.all()
    settings_dic = {}
    for setting in settings:
        settings_dic[setting.name] = setting.value
    return settings_dic


import contact


## Custom error handling ##

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

