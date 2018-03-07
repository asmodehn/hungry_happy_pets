import unittest
import json

from hypothesis import given
import hypothesis.strategies as st

try:
    from .utils import clean_memorydb_session_from_schema
except SystemError:
    from utils import clean_memorydb_session_from_schema

from app.schemas import models, species_schema


@given(name=st.text(),
       happy_rate=st.integers(min_value=-2147483648, max_value=2147483647),  # SQL INTEGER range
       hunger_rate=st.integers(min_value=-2147483648, max_value=2147483647),  # SQL INTEGER range
)
def test_load_dump_species(name, happy_rate, hunger_rate):

    with clean_memorydb_session_from_schema(species_schema) as s:

        ori = {'name': name, 'happy_rate': happy_rate, 'hunger_rate': hunger_rate}

        # load our dict
        species_data, species_errors = species_schema.load(ori, session=s)

        # check we can save it
        species_data.save(session=s)

        # retrieve it again
        species_stored = s.query(models.Species).get(species_data.id)

        # compare models
        assert species_data == species_stored

        # serialize
        fin, err = species_schema.dump(species_stored)

        # pop the added id
        assert 'id' in fin
        fin.pop('id')

        # compare dicts
        assert ori == fin

