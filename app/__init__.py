from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_migrate import Migrate
from flask_mail import Mail
from config import config



db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()
migrate = Migrate()
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    
    # Φόρτωση config
    app.config.from_object(config[config_name])
    
    # hook for specific env setup
    config[config_name].init_app(app)
    
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    
    return app
    
    