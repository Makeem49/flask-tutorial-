from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, SelectField
from wtforms.validators import Required, Length, EqualTo, Email, ValidationError, InputRequired 
from app.models import User
from flask_pagedown.fields import PageDownField

class NameForm(FlaskForm):
	name = StringField('name', validators=[Required(), Length(min=1,max=64), Email()])
	submit = SubmitField("Log In")	


class LoginForm(FlaskForm):
	email = StringField('email', validators=[Required(), Length(4,64), Email()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Remember me')
	submit = SubmitField("Log In")	


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators = [Required(), Length(min=4, max=25)])
	email = StringField('Email Address', validators = [Required(), Email()])
	password = PasswordField('Password', validators = [InputRequired(), Length(min=4), EqualTo("password")])
	confirm_password = PasswordField("Confirm Password", validators = [InputRequired()])
	submit = SubmitField("Sign Up")

	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("Username already exist")

	def validate_email(self,email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("Email already taken")

class PasswordUpdate(FlaskForm):
	old_password = PasswordField('Old Password', validators=[Required()])
	password = PasswordField('New Passowrd', validators = [Required(), Length(min=4)])
	confirm_password = PasswordField("Confirm New Password", validators = [Required(), EqualTo("password")])
	submit = SubmitField("Update Password")


class ResetPasswordLink(FlaskForm):
	email = StringField('Email Address', validators = [Required(), Email()])
	submit = SubmitField("Send Password reset Link")

	def validate_email(self,email):
		user = User.query.filter_by(email=email.data).first()
		if not user:
			raise ValidationError("There is no account with this email, you must register first.")


class NewPasswordLForm(FlaskForm):
	password = PasswordField('New Passowrd', validators = [Required(), Length(min=4)])
	confirm_password = PasswordField("Confirm New Password", validators = [Required(), EqualTo("password")])
	submit = SubmitField("Reset Password")


class UpdateMail(FlaskForm):
	old_mail = StringField('Current Email', validators=[Required(), Email()])
	new_mail = StringField('New Email', validators = [Required(), Email()])
	submit = SubmitField("Update Email")

	def validate_email(self, new_mail):
		user = User.query.filter_by(email = new_mail.data).first()
		if user:
			raise ValidationError('Email already taken')


class EditProfileForm(FlaskForm):
	name = StringField("Real name", validators=[Length(min=1,max =64)])
	location = StringField('Location', validators=[Length(min=1, max = 64)])
	about_me = TextAreaField("About me")
	submit = SubmitField("Submit")



class EditProfileAdminForm(FlaskForm):
	name = StringField("Real name", validators=[Length(min=1, max=64)])
	username = StringField("Username", validators=[Length(min=4, max=64)])
	email = StringField("Email", validators=[Required(), Length(min=4, max=64), Email()])
	Confirmed = BooleanField('Confirmed')
	role = SelectField("Role", coerce=int)
	location = StringField("Location", validators=[Length(min=1,max=64)])
	about_me = TextAreaField("About me")
	submit = SubmitField("Submit")


	def __init__(self,user,*args,**kwargs):
		super().__init__(*args , **kwargs)
		self.role.choice = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
		self.user = user

	def validate_email(self, email):
		if email.data != self.user.email and User.query.filter_by(email = email.data).first():
			raise ValidationError("Email already registered")

	def validate_email(self, username):
		if username.data != self.username.email and User.query.filter_by(email = username.data).first():
			raise ValidationError("Username already registered")


class PostForm(FlaskForm):
    body = PageDownField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')





