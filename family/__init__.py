from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from family.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config) # getting configuration from config.py file
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    with app.app_context():
        from family import routes
        db.create_all()
        
        return app
