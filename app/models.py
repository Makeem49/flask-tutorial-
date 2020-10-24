from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin 
from app import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app



@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class Role(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key= True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref='role',  lazy='dynamic')

	def __repr__(self):
		return f"Role {self.name}"


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(64), unique=True, index=True) 
	username = db.Column(db.String(64), unique = True, index = True) 
	password_hash = db.Column(db.String(128))
	role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
	confirmed = db.Column(db.Boolean, dafault = False)

	@property #This will genearte a write only property field
	def password(self):
		raise AttributeError('Password is not readable attribute')

	@password.setter  # setting setter on password helps to prevent the password from being read once hashed and store it in the password_hash filed  
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def generate_confirmation_token(self, expiration = 3600):
		s = Serializer(current_app.config['SECRET_KEY'], expires_in = expiration)
		return s.dumps({'user_id' : self.id})

	def confirm(self,token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False

		if data.get('user_id') != self.id:
			return False
		self.confirmed = True
		db.session.add(self)
		
		return True

	def __repr__(self):
		return f"User {self.username}"