"""
A package to do everything database related
This needs to be separated from schemas to avoid circular imports.
"""

from ._bootstrap import db
from .animals import Animal
from .owners import Owner
from .species import Species
from .users import User

