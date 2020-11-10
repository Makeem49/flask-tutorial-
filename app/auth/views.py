from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.auth import auth
from app.models import User
from app.main.forms import (LoginForm, RegistrationForm, PasswordUpdate, 
												UpdateMail,ResetPasswordLink, NewPasswordLForm)
from app import db
from app.email import send_email



'''This function collect all the necessery detaiils the usere need to create an account'''
@auth.route('/register', methods=['GET', 'POST']) 
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email(user.email, 'Confirm Your Account','auth/email/confirm', user=user, token=token)
		return redirect(url_for("auth.login"))
	return render_template('auth/register.html', form = form, title = 'Register page')



'''The login view function verify the user account credentials before given access to login the account'''
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
			flash('There is no account with this account, You need to register first')
		else:
			flash('Invalid username or password')
	return render_template('auth/login.html', title = "login", form = form)


'''The view function can only be accessed if the user is login '''
@auth.route('/logout')
@login_required
def logout():
    logout_user()    
    flash('You have been logged out.')    
    return redirect(url_for('auth.login'))


'''This view function verify if the user can be reached by email they provided when they register their account
and that account must be able to recieve a confirmation mail'''
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash('Your account has been confirmed. Thanks', 'success')
	else:
		flash('The confirmation link has expired or invalid', 'danger')
	return redirect(url_for('main.index'))

'''This view function help to determine what unconfirmed user can do when tey login.
That it restrict the user navigation on website '''
@auth.before_app_request
def before_request():
	if current_user.is_authenticated and not current_user.confirmed and request.blueprint != 'auth':
		return redirect(url_for('auth.unconfirmed'))

'''This view function tell what the unconfirmed user needs to do to confim their account '''
@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')


'''This view function is also included in the unconfirmed page. In case the user token is expired or the confirmation link was lost, user can request for another for another confirmation link '''
@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email,'Confirm Your Account', 'auth/email/confirm', user = current_user , token = token )
	flash('A new confirmation email has been sent to your by email')
	return redirect(url_for('main.index'))

'''This view func help the user to change their account password for security purpose.'''
@auth.route('/password', methods=['GET', 'POST'])
@login_required
def change_password():
	form = PasswordUpdate()
	if form.validate_on_submit():
		if current_user.verify_password(form.old_password.data):
			current_user.password = form.password.data
			db.session.commit()
			flash('Your password has been successfully updated')
			return redirect(url_for('main.index'))
		else:
			flash('Incorrect password')
	return render_template('change_password.html', form = form)


'''This view function is the one the user will access through it's email provided to receive a link to reset his/her 
password. '''
@auth.route('/password_link', methods=['GET', 'POST'])
def reset_password_link():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = ResetPasswordLink()
	if form.validate_on_submit():
		user = User.query.filter_by(email =form.email.data).first()
		token = user.generate_confirmation_token()
		send_email(user.email,'Confirm Your Account', 'auth/email/confirm', user = user , token = token )
		flash('Password reset link has been sent to your email.', 'success')
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password_link.html', form = form)


'''This view func verify may the user link send to the email provided is valid or not '''
@auth.route('/password_link/<token>', methods=['GET', 'POST']) 
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	if current_user.confirm(token):
		flash('Your can set a new password for your account')
		return redirect(url_for('new_password'))
	else:
		flash('The confirmation link has expired or invalid', 'info')
	return redirect(url_for('main.index'))


'''This func handle users password updating in case they forget their account.'''
@auth.route('/new_password', methods=['GET', 'POST'])
def new_password():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = NewPasswordLForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.data.email).first()
		user.password = form.password.data
		db.session.commit()
		flash('You have successfully change your password')
		return redirect(url_for('auth.login'))
	return render_template('auth/new_password.html', form = form )



@auth.route('/update_email', methods=['GET', 'POST'])
@login_required
def update_email():
	form = UpdateMail()
	if form.validate_on_submit():
		if current_user.email == form.old_mail.data:
			current_user.email = form.new_mail.data
			db.session.commit()
			token = user.generate_confirmation_token()
			send_email(current_user.email,'Confirm Your Account', 'auth/email/email_confirm', user = user , token = token )
			flash('A confirmation link has been sent to your new email address.')
			return redirect(url_for('main.index'))			
		else:
			flash('Please provide your current email address.')
	return render_template('auth/update_email.html', form = form )


@auth.route('/confirm_new_email/<token>', methods=['GET', 'POST']) 
def confirm_new_email(token):
	if current_user.confirm(token):
		flash('Your new email has been successfully verified.','success')
		return redirect(url_for('main.index'))
	else:
		flash('The confirmation link has expired or invalid', 'info')
	return redirect(url_for('main.index'))







