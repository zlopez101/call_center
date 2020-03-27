from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from ut.config import Config

# for db updating...

#app = Flask(__name__)
#app.config.from_object(Config)
#db = SQLAlchemy(app)
#login_manager = LoginManager(app)
#bcrypt = Bcrypt(app)


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "employee.login"
login_manager.login_message_category = "info"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    from ut.call_center.routes import call_center
    from ut.employee.routes import employee
    from ut.public.routes import public
    from ut.confirmations.routes import confirmations

    app.register_blueprint(public)
    app.register_blueprint(employee)
    app.register_blueprint(call_center)
    app.register_blueprint(confirmations)
    return app

