from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class NameForm(Form):
	email = StringField('email', validators=[DataRequired(), Length(4,64), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField("Log In")	





