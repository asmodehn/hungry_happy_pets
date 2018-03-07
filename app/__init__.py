from flask_api import FlaskAPI

# DB design :
# Users 1-1 Owner
# Animals *-1 Race
# Animals *-1 Owner
# TODO : nice entity association ascii art

# Note here we try to keep a bijective ORM - Schema - REST resource relationship, to keep app structure simple

from .schemas import models, ma
from .animals import animals, animals_detail
from .species import species, species_read, species_edit, species_add, species_delete
from .owners import owners, owner_read, owner_edit, owner_add, owner_delete
from .users import users, user_read, user_edit, user_add, user_delete

# local import
from instance.config import app_config


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)  # __name__ is required to find the instance folder

    # http://flask.pocoo.org/docs/0.12/config/
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    models.db.init_app(app)
    ma.init_app(app)

    # setup routing (has to be done dynamically, and not on import).
    # TODO : api in blue print... ( check with flask api )
    app.add_url_rule('/api/users/', view_func=users)
    app.add_url_rule('/api/users/<id>', view_func=user_read, methods=["GET"])
    app.add_url_rule('/api/users/<id>', view_func=user_edit, methods=["PUT"])
    app.add_url_rule('/api/users/', view_func=user_add, methods=["POST"])
    app.add_url_rule('/api/users/<id>', view_func=user_delete, methods=["DELETE"])

    app.add_url_rule('/api/owners/', view_func=owners)
    app.add_url_rule('/api/owners/<id>', view_func=owner_read, methods=["GET"])
    app.add_url_rule('/api/owners/<id>', view_func=owner_edit, methods=["PUT"])
    app.add_url_rule('/api/owners/', view_func=owner_add, methods=["POST"])
    app.add_url_rule('/api/owners/<id>', view_func=owner_delete, methods=["DELETE"])

    app.add_url_rule('/api/species/', view_func=species)
    app.add_url_rule('/api/species/<id>', view_func=species_read, methods=["GET"])
    app.add_url_rule('/api/species/<id>', view_func=species_edit, methods=["PUT"])
    app.add_url_rule('/api/species/', view_func=species_add, methods=["POST"])
    app.add_url_rule('/api/species/<id>', view_func=species_delete, methods=["DELETE"])

    app.add_url_rule('/api/animals/', view_func=animals)
    app.add_url_rule('/api/animals/<id>', view_func=animals_detail)

    return app
