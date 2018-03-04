"""
A custom package to do all required import time initialization, flask plugin style
"""

from flask_sqlalchemy import SQLAlchemy

# initialize sql-alchemy
db = SQLAlchemy()


from flask_marshmallow import Marshmallow


# initialize marshmallow
ma = Marshmallow()
