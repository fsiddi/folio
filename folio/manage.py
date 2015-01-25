import os
from application import app, db
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

manager = Manager(app)

# alembic migrations
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def create_all_tables():
	"""Creates all tables"""
	db.create_all()

manager.run()
