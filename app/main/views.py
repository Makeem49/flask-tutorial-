from datetime import datetime
from flask import render_template, url_for, redirect, session, flash
from app.main.forms import NameForm
from app import db 
from app.models import User
from app.main import main



@main.route('/', methods=['POST', 'GET'])  
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
		return redirect(url_for('main.index'))
	return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False)) 





