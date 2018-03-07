import unittest
import json

from hypothesis import given
import hypothesis.strategies as st

try:
    from .utils import clean_memorydb_session_from_schema
except SystemError:
    from utils import clean_memorydb_session_from_schema

from app.schemas import models, user_schema


@given(nick=st.text(), email=st.text())
def test_load_dump_users(nick, email):

    with clean_memorydb_session_from_schema(user_schema) as s:

        ori = {'nick': nick, 'email': email}

        # load our dict
        user_data, user_errors = user_schema.load(ori, session=s)

        # check we can save it
        user_data.save(session=s)

        # retrieve it again
        user_stored = s.query(models.User).get(user_data.id)

        # compare models
        assert user_data == user_stored

        # serialize
        fin, err = user_schema.dump(user_stored)

        # pop the added id
        assert 'id' in fin
        fin.pop('id')

        # compare dicts
        assert ori == fin


