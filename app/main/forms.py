from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Length, EqualTo, Email, ValidationError
from app.models import User



class NameForm(Form):
	name = StringField('name', validators=[Required(), Length(4,64), Email()])
	submit = SubmitField("Log In")	



class LoginForm(Form):
	email = StringField('email', validators=[Required(), Length(4,64), Email()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Remember me')
	submit = SubmitField("Log In")	


class RegistrationForm(Form):
	username = StringField('Username', validators = [Required(), Length(min=4, max=25)])
	email = StringField('Email Address', validators = [Required(), Email()])
	password = PasswordField('Password', validators = [Required(), Length(min=4)])
	confirm_password = PasswordField("Confirm Password", validators = [Required(), EqualTo("password")])
	submit = SubmitField("Sign Up")

	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("Username already exist")

	def validate_email(self,email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("Email already taken")

class Password_Update(Form):
	old_password = PasswordField('Old Password', validators=[Required()])
	password = PasswordField('New Passowrd', validators = [Required(), Length(min=4)])
	confirm_password = PasswordField("Confirm New Password", validators = [Required(), EqualTo("password")])
	submit = SubmitField("Update Password")


class Reset_Password_link(Form):
	email = StringField('Email Address', validators = [Required(), Email()])
	submit = SubmitField("Send Password reset Link")

	def validate_email(self,email):
		user = User.query.filter_by(email=email.data).first()
		if not user:
			raise ValidationError("There is no account with this email, you must register first.")


class New_Password_Form(Form):
	password = PasswordField('New Passowrd', validators = [Required(), Length(min=4)])
	confirm_password = PasswordField("Confirm New Password", validators = [Required(), EqualTo("password")])
	submit = SubmitField("Reset Password")


class Update_Mail(Form):
	old_mail = StringField('Current Email', validators=[Required(), Email()])
	new_mail = StringField('New Email', validators = [Required(), Email()])
	submit = SubmitField("Update Email")

	def validate_email(self, new_mail):
		user = User.query.filter_by(email = new_mail.data).first()
		if user:
			raise ValidationError('Email already taken')