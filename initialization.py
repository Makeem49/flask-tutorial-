from flask import Flask, request, make_response, abort, render_template, redirect,url_for,session

from flask_bootstrap import Bootstrap  #this is a flask-boostrap extension 
from flask_moment import Moment
from datetime import datetime
from form import NameForm

#initialization of Flask
app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = '0fb7ef58e49e4a7d83898e93ae3033e3'




# Setting route & view function 
@app.route("/", methods=['GET', 'POST']) 
def index():
	form = NameForm()
	# name = ''
	if form.validate_on_submit():
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
