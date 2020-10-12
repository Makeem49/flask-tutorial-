from flask import Flask, render_template, url_for, redirect, session, flash
from flask_moment import Moment
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import os
from flask_script import Shell
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail





app = Flask(__name__)
app.config['SECRET_KEY'] = '4c80d06c39bce18f8556ab068f80caf9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
mail = Mail(app)

db = SQLAlchemy(app)
manager = Manager(app)
moment = Moment(app)
bootstrap = Bootstrap(app)


app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')




class Role(db.Model):
	id = db.Column(db.Integer, primary_key= True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref='role',  lazy='dynamic')

	def __repr__(self):
		return f"Role {self.name}"


class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), unique = True, index = True)
	role_id = db.Column(db.Integer, db.ForeignKey('role.id')) 

	def __repr__(self):
		return f"User {self.username}"



class NameForm(Form):
	name = StringField('What is your name?', validators=[DataRequired()])
	submit = SubmitField('Submit')





@app.route('/', methods=['POST', 'GET'])  
def index():
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username=form.name.data)
			db.session.add(user)
			session['know'] = False
		else:
			session['know'] = True
		session['name'] = form.name.data 
		form.name.data = ''
		return redirect(url_for('index'))
	return render_template('index.html', title = "home",
		know = session.get('know', False) ,name =session.get("name"), form = form)  


@app.route('/user/<name>') 
def user(name):    
	return render_template('user.html', name = name)

@app.errorhandler(500) 
def page_not_found(e): 
	return render_template('500.html', title = "Server Error"), 500

@app.errorhandler(404) 
def page_not_found(e): 
	return render_template('404.html', title = "Page Error"), 404


def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)
manager.add_command('shell', Shell(make_context=make_shell_context))

migrate = Migrate(app,db)
manager.add_command('db', MigrateCommand)








if __name__ == '__main__':
    manager.run()