import os
from application import app, db
from flask.ext.script import Manager

manager = Manager(app)

@manager.command
def create_all_tables():
	"""Creates all tables"""
	db.create_all()

manager.run()
