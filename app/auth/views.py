from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.auth import auth
from app.models import User
from app.main.forms import LoginForm, RegistrationForm
from app import db
from app.email import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect('main.index')
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			flash('You are now logged in', 'success')
			login_user(user, remember = form.remember_me.data)
			next_page = request.args.get('next')   # Using request.atgs.get("next") to query if there's next page, will direct us to the page if it exist na d none if it does not
			if next_page:
				return redirect(next_page)
			else: 
				return redirect(url_for('main.index'))
		elif user is None:
			flash('There is no email with that account, You need to register first')
		else:
			flash('Invalid username or password')
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
		send_email(user.email, 'Confirm Your Account','auth/email/confirm', user=user, token=token)
		flash('A confirmation email has been sent to your mail.')
		return redirect(url_for("auth.login"))
	return render_template('auth/register.html', form = form, title = 'Register page')


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	elif current_user.confirm(token):
		flash('Your account has been confirmed. Thanks', 'success')
	else:
		flash('The confirmation link has expired or invalid', 'success')
	return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
	if current_user.is_authenticated and not current_user.confirmed and request.blueprint != 'auth':
		return redirect(url_for('auth.unconfirmed'))



@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect('main.index')
	return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email,'Confirm Your Account', 'auth/email/confirm', user = current_user , token = token )
	flash('A new confirmation email has been sent to your by email')
	return render_template('auth/resend_confirmation.html')


