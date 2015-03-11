from flask import render_template, Blueprint

from application import app, db
from application.modules.pages.model import Page
from application.modules.theme import get_theme_dir

pages = Blueprint('pages', __name__)


@pages.route('/<url>')
def view(url):
    page = Page.query.filter_by(url=url).first_or_404()   
    return render_template(get_theme_dir() + '/page.html',
        content=page.content,
        title=page.url)
