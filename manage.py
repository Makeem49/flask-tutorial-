import os 
from app import create_app, db 
from app.models import User, Role, Post, Follow, fake_attribute
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app('default') 
migrate = Migrate(app,db)
manager = Manager(app)


def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role, Post= Post, Follow = Follow, fake_attribute=fake_attribute)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command 
def test():
	'''Run the units tests.'''
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)



if __name__ == '__main__':
    manager.run()

