"""
A custom package to do all required import time initialization, flask plugin style
"""

from flask_sqlalchemy import SQLAlchemy

# initialize sql-alchemy
db = SQLAlchemy()


from flask_marshmallow import Marshmallow


# initialize marshmallow
ma = Marshmallow()


def init(app):
    # Order matters: Initialize SQLAlchemy before Marshmallow
    db.init_app(app)
    ma.init_app(app)
    # remember sqlalchemy-marshmallow is required in order to integrate between both flask addons
