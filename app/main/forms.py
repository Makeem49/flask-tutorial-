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
	email = StringField('Email', validators=[Required(), Length(4,64), Email()])
	username = 	StringField('Username' , validators=[Required(), Length(4,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Usernames must have only letters, '
																					'numbers, dots or underscores')])
	password = PasswordField('Password', validators=[Required(), EqualTo('Confirm_Password', message='Password must match.')])
	confirm_password =  PasswordField('Confirm Password', validators=[Required()])
	submit = SubmitField('Register')


	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if user:
			raise validationError('Email already taken')

	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()
		if user:
			raise validationError('Username already already in use.')

