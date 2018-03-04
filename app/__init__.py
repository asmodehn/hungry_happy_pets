from flask_api import FlaskAPI

# DB design :
# Users 1-1 Owner
# Animals *-1 Race
# Animals *-1 Owner
# TODO : nice entity association ascii art

from .addons import db, ma
from .users import users, user_detail
from .owners import owners, owner_detail
from .species import species, species_detail
from .animals import animals, animals_detail

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

    # setup routing (has to be done dynamically, and not on import).
    app.add_url_rule('/api/users/', view_func=users)
    app.add_url_rule('/api/users/<id>', view_func=user_detail)

    app.add_url_rule('/api/owners/', view_func=owners)
    app.add_url_rule('/api/owners/<id>', view_func=user_detail)

    app.add_url_rule('/api/species/', view_func=species)
    app.add_url_rule('/api/species/<id>', view_func=user_detail)

    app.add_url_rule('/api/animals/', view_func=species)
    app.add_url_rule('/api/animals/<id>', view_func=user_detail)

    return app
