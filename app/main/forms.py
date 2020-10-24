from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Length, EqualTo, Email, ValidationError, Regexp


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
	confirm_password = PasswordField("Confirm Password", validators = [Required(), EqualTo("password",  message='Passwords must match.')])
	submit = SubmitField("Sign Up")

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if user:
			raise ValidationError('Email already taken')

	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()
		if user:
			raise ValidationError('Username already already in use.')

