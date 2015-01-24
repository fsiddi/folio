from flask import render_template
from application import app

from application.models.model import Setting

theme_setting = Setting.query.filter_by(name='folio_theme').first()
if theme_setting:
    theme = str(theme_setting)
else:
	theme = app.config['THEME']
THEME_DIR = theme + '/'



## Custom error handling ##

@app.errorhandler(404)
def page_not_found(error):
    return render_template(THEME_DIR + 'error.html', code="404", desc="Page not Found"), 404

@app.errorhandler(403)
def forbidden(error):
    return render_template(THEME_DIR + 'error.html', code="403", desc="Forbidden"), 403

@app.errorhandler(401)
def not_authorized(error):
    return render_template(THEME_DIR + 'error.html', code="401", desc="Not Authorized"), 401

