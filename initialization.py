from flask import Flask, request, make_response, abort, render_template, redirect,url_for,session, flash
from flask_bootstrap import Bootstrap  #this is a flask-boostrap extension 
from flask_moment import Moment
from datetime import datetime
from form import NameForm
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import os 
from flask_mail import Mail


#initialization of Flask
app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


app.config['SECRET_KEY'] = '0fb7ef58e49e4a7d83898e93ae3033e3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587 
app.config['MAIL_USE_TLS']	= True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)
db = SQLAlchemy(app)

migrate = Migrate(app,db)
manager.add_command('db', MigrateCommand)

class Role(db.Model):
	__tablename__ = "roles" 
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String , unique = True, nullable = False)
	users = db.relationship("User", backref = "role", lazy = 'dynamic')

	def __repr__(self):
		return f"Role {self.name}"


class User(db.Model):
	__tablename__ = "users" 
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String, unique = True, nullable = False)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  #The arguemnt in foreign_key use the Role table name from Role class


	def __repr__(self):
		return f"User {self.username}"




# Setting route & view function 
@app.route("/", methods=['GET', 'POST']) 
def index():
	form = NameForm()
	# name = ''
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username=form.name.data)
			db.session.add(user)
			db.session.commit()
			session['known'] = False
		else:
			session['known'] = True
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('index'))
	return render_template("index.html", form = form, name=session.get('name'),
															known = session.get("known", False))

@app.route("/user/<name>")  # setting dynamic route
def user(name):
	form = NameForm()
	return render_template('login.html', name=name, form=form)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)

manager.add_command('shell', Shell(make_context = make_shell_context))





# Server set up 
if __name__ == "__main__":    
    manager.run()
	# app.run(debug=True)																				