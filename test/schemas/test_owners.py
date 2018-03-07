import unittest
import json

from hypothesis import given
import hypothesis.strategies as st

try:
    from .utils import clean_memorydb_session_from_schema
except SystemError:
    from utils import clean_memorydb_session_from_schema

from app.schemas import animal_schema, species_schema

def test_load_animals_species_id():

    with clean_memorydb_session_from_schema(animal_schema) as s:

        # load our dict
        animal_data, animal_errors = animal_schema.load({'name': 'testanimal', 'happy': 4, 'hungry': 42}, session=s)

        # check we canNOT save it
        animal_data.save(session=s)
