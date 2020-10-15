from flask import Flask, render_template
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from config import config
from flask_sqlalchemy import SQLAlchemy





mail = Mail()
db = SQLAlchemy()
moment = Moment()
bootstrap = Bootstrap()



def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	mail.init_app(app)
	db.init_app(app)
	moment.init_app(app)
	bootstrap.init_app(app)

	from app.main import main as main_blueprint
	app.register_blueprint(main_blueprint)


	return app