from flask import Flask, request, make_response, abort, render_template, redirect,url_for,session, flash
from flask_bootstrap import Bootstrap  #this is a flask-boostrap extension 
from flask_moment import Moment
from datetime import datetime
from form import NameForm
from flask_sqlalchemy import SQLAlchemy

#initialization of Flask
app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = '0fb7ef58e49e4a7d83898e93ae3033e3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 

db = SQLAlchemy(app)

class Role(db.Model):
	__tablename__ = "roles" 
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String , unique = True, nullable = False)
	users = db.relationship("User", backref = "role", backref = 'dynamic')

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
		old_name = session.get('name')
		if old_name is not None and old_name != form.name.data:
			flash('username not matched, please check your spelling!')
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('index'))
	return render_template("index.html", form = form, name=session.get('name'))

@app.route("/user/<name>")  # setting dynamic route
def user(name):
	form = NameForm()
	return render_template('login.html', name=name, form=form)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

# Server set up 
if __name__ == "__main__":
	app.run(debug=True)
