from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from ut.config import Config

#for db updating...
#app = Flask(__name__)
#app.config.from_object(Config)
#db = SQLAlchemy(app)
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager.login_view = "login"
login_manager.login_message_category = "info"


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	from ut.calls.routes import calls
	from ut.employees.routes import employees
	from ut.website.routes import website
	
	app.register_blueprint(website)
	app.register_blueprint(employees)
	app.register_blueprint(calls)
	return app
