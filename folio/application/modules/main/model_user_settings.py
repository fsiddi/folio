from application import app
from application import db

from flask.ext.login import UserMixin


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


class Setting(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable=False)
    value = db.Column(db.String(256), nullable=False)

    def __str__(self):
        return str(self.value)


class SocialLink(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    order = db.Column(db.Integer)
    icon = db.Column(db.String(16), nullable=False)
    handle = db.Column(db.String(128), nullable=False)
    href = db.Column(db.String(128), nullable=False)


