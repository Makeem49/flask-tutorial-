from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from app import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from datetime import datetime
import hashlib



@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class Permission:
	FOLLOW = 0x01 
	COMMENT = 0X02
	WRITE_ARTICLES = 0X04
	MODERATE_COMMENT = 0X08
	ADMINISTER = 0X80


class Role(db.Model, UserMixin):
	__tablename__ = 'roles' 
	id = db.Column(db.Integer, primary_key= True)
	name = db.Column(db.String(64), unique=True)
	default = db.Column(db.Boolean, default = False, index = True)
	permissions = db.Column(db.Integer)
	users = db.relationship('User', backref='role',  lazy='dynamic')
 

	@staticmethod 
	def  insert_roles():
		roles = {
			'User':(Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES, True),
			'Moderator':(Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES | Permission.MODERATE_COMMENT, False),
			'Administrator': (0xff, False)
		}
		for r in roles:
			role = Role.query.filter_by(name = r).first()
			if role is None:
				role = Role(name=r)
			role.permissions = roles[r][0]
			role.default = roles[r][1]
			db.session.add(role)
		db.session.commit()

	def __repr__(self):
		return f"Role {self.name}"


class Post(db.Model, UserMixin):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.Text, nullable = False)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow, index = True)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class User(db.Model, UserMixin):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(64), unique=True, index=True) 
	username = db.Column(db.String(64), unique = True, index = True) 
	password_hash = db.Column(db.String(128))
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	confirmed = db.Column(db.Boolean, default = False )
	name = db.Column(db.String(64))
	location = db.Column(db.String(64))
	about_me = db.Column(db.Text())
	member_since = db.Column(db.DateTime(), default = datetime.utcnow )
	last_seen = db.Column(db.DateTime(), default = datetime.utcnow )
	avatar_hash = db.Column(db.String(32))
	posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')


	def ping(self):
		self.last_seen = datetime.utcnow()
		db.session.add(self)


	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		if self.role is None:
			if self.email == current_app.config['FLASKY_ADMIN']:
				self.role = Role.query.filter_by(permissions = 0xff).first()
			if self.role  is None:
				self.role = Role.query.filter_by(default = True).first()

		if self.email is not None and self.avatar_hash is None:
			self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()


	def can(self, permissions):
		return self.role is not None and (self.role.permissions & permissions) == permissions

	def is_admistrator(self):
		return self.can(Permission.ADMINISTER)



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


	def change_email(self, token):
		self.email = new_email
		self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
		db.session.commit()
		return True

	def gravatar(self, size=100, default='identicon', rating = 'g'):
		if request.is_secure:
			url = 'https://secure.gravater.com/avatar'
		else:
			url = 'http://secure.gravater.com/avatar'
		hash = self.avatar_hash or hashlib.md5(user.email.encode('utf-8')).hexdigest()
		return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=hash,
												 size=size, default=default, rating=rating)


	def __repr__(self):
		return f"User {self.username}"


class AnonymousUser(AnonymousUserMixin):
	def can(self,permissions):
		return False

	def is_admistrator(self):
		return False


		
login_manager.anonymous_user = AnonymousUser








