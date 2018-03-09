"""
A package to do everything database related
This needs to be separated from schemas to avoid circular imports.
"""

from ._bootstrap import db
from .animals import Animal
from .owners import Owner
from .species import Species
from .users import User


from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(name='happy-hungry-pets', template_mode='bootstrap3')

# Add administrative views here
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Owner, db.session))
admin.add_view(ModelView(Species, db.session))
admin.add_view(ModelView(Animal, db.session))
