from flask import Flask, render_template
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager




mail = Mail()
db = SQLAlchemy()
moment = Moment()
bootstrap = Bootstrap()

login_manager = LoginManager()
login_manager.session_protection = 'strong' # The strong value keep track of the Clients IP address
login_manager.login_view = 'auth.login'
login_manager.login_message = 'You have to login to access this page'
login_manager.login_message_category = 'info'


def create_app(default):
	app = Flask(__name__)
	app.config.from_object(config[default])
	config[default].init_app(app)

	mail.init_app(app)
	db.init_app(app)
	moment.init_app(app)
	bootstrap.init_app(app)
	login_manager.init_app(app)

	from app.main import main as main_blueprint
	from app.auth import auth as auth_blueprint
	app.register_blueprint(main_blueprint)
	app.register_blueprint(auth_blueprint, url_prefix ='/auth')

	return app





