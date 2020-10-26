from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.auth import auth
from app.models import User
from app.main.forms import LoginForm, RegistrationForm
from app import db



@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			flash('You are now logged in', 'success')
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
		user = User(username=form.username.data, email=form.email.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		return redirect(url_for("auth.login"))
	return render_template('auth/register.html', form = form, title = 'Register page')


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash('Your account has been confirmed. Thanks', 'success')
	else:
		flash('The confirmation link has expired or invalid', 'success')
	return redirect(url_for('main.index'))

