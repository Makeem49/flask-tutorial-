from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField
from wtfroms.validators import Required 

class NameForm(Form):
	name = StringField("what is your name ", validators=[Required()]
	submit = SubmitField("Submit")












