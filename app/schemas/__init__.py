"""
A package to do everything schemas related
This needs to be separated from models to avoid circular imports.
"""


from . import models

from ._bootstrap import ma

from .users import user_schema
from .owners import owner_schema
from .species import species_schema
from .animals import animal_schema
