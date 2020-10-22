import os 



basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
	FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
	FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	
	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

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




