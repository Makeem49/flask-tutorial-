import os 



basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
	FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
	FLASKY_ADMIN = 'patrickpwilliamson9@gmail.com'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	FLASKY_POSTS_PER_PAGE = 20
	
	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = 'smtp.gmail.com' 
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USE_SSL = False
	MAIL_USERNAME = 'patrickpwilliamson9@gmail.com'
	MAIL_PASSWORD = 'Olayinka1'
	MAIL_DEFAULT_SENDER = 'patrickpwilliamson9@gmail.com'
	MAIL_MAX_EMAILS = 5
	MAIL_SUPPRESS_SEND = False
	MAIL_ASCII_ATTACHMENTS = False
	SQLALCHEMY_DATABASE_URI =  'sqlite:///' + os.path.join(basedir, 'data.sqlite') 

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI =  'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI =  'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
	'development' : DevelopmentConfig,
	'testing' : TestingConfig,
	'production' : ProductionConfig,


	'default' : DevelopmentConfig
}




