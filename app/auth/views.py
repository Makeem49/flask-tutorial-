from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from app.auth import auth
from app.models import User
from app.main.forms import LoginForm, RegistrationForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			next_page = request.args.get('next')   # Using request.atgs.get("next") to query if there's next page, will direct us to the page if it exist na d none if it does not
			if next_page:
				return redirect(next_page)
			else: 
				return redirect(url_for('main.index'))
		flash('Invalid username or password.')
	return render_template('auth/login.html', title = "login",form = form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()    
    flash('You have been logged out.')    
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST']) 
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data, username=form.username.data, password_hash = form.password.data)
		db.session.add(user)
		flash('Congratulations, you are now a registered user!', 'success')
		return redirect(url_for('login'))
	return render_template('auth/register.html', form = form, title = 'Register page')


