from flask import Flask, render_template, url_for, redirect, session, flash
from flask_moment import Moment
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class NameForm(Form):
	name = StringField('What is your name?', validators=[Required()])
	submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = '4c80d06c39bce18f8556ab068f80caf9'
moment = Moment(app)
bootstrap = Bootstrap(app)


@app.route('/', methods=['POST', 'GET'])  
def index():
	form = NameForm()
	if form.validate_on_submit():
		old_name = session.get('name')
		if old_name is not None and old_name != form.name.data:
			flash("Looks like you've changed your username")
		session['name'] = form.name.data 
		return redirect(url_for('index'))
	return render_template('index.html', title = "home", name =session.get("name"), form = form)  

@app.route('/user/<name>') 
def user(name):    
	return render_template('user.html', name = name)

@app.errorhandler(500) 
def page_not_found(e): 
	return render_template('500.html', title = "Server Error"), 500

@app.errorhandler(404) 
def page_not_found(e): 
	return render_template('404.html', title = "Page Error"), 404

if __name__ == '__main__':
    app.run(debug=True)