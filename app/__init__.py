from flask_api import FlaskAPI

from .models import db
from .schemas import ma
from . import views

# local import
from instance.config import app_config


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)

    # http://flask.pocoo.org/docs/0.12/config/
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Order matters: Initialize SQLAlchemy before Marshmallow
    db.init_app(app)
    ma.init_app(app)

    return app, db
