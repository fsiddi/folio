from application import app
from application.modules.main.model_user_settings import Setting


def get_theme_dir():
    #query the theme
    theme_setting = Setting.query.filter_by(name='folio_theme').first()
    if theme_setting:
        theme = str(theme_setting)
    else:
        theme = app.config['THEME']

    THEME_DIR = theme + '/'
    return THEME_DIR


# TODO interface for changing theme

# TODO user interface for managing the theme
