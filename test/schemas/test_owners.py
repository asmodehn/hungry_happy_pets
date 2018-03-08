import pytest
import json

from hypothesis import given
import hypothesis.strategies as st

try:
    from .utils import clean_memorydb_session_from_schema, dummy_user
except SystemError:
    from utils import clean_memorydb_session_from_schema, dummy_user

from app.schemas import models, user_schema, owner_schema


#@given()
def test_load_dump_owners_user_id():

    with clean_memorydb_session_from_schema(owner_schema) as s:

        with dummy_user(s) as user:

            ori = {'user_id': user.id}

            # load our dict
            owner_data, owner_errors = owner_schema.load(ori, session=s)

            # check we can save it
            owner_data.save(session=s)

            # retrieve it again
            owner_stored = s.query(models.Owner).get(owner_data.id)

            # compare models
            assert owner_stored == owner_data

            # serialize
            fin, err = owner_schema.dump(owner_stored)

            # pop the added id
            assert 'id' in fin
            fin.pop('id')

            # compare dicts
            # user_id should have been expanded to the dummy user
            assert fin.get('user') == user_schema.dump(user).data
            fin.pop('user')
            # the rest should be identical
            ori.pop('user_id')
            assert fin == ori

            # deleting table before removing dummy user
            owner_stored.delete(session=s)


def test_load_owners_NO_user_id_FAIL():

    with clean_memorydb_session_from_schema(owner_schema) as s:

        ori = {}

        # load our dict
        owner_data, owner_errors = owner_schema.load(ori, session=s)

        # assert we can NOT save it
        with pytest.raises(Exception):
            owner_data.save(session=s)


def test_load_owners_user_FAIL():

    with clean_memorydb_session_from_schema(owner_schema) as s:

        with dummy_user(s) as user:

            ori = {'user': user}

            # load our dict
            owner_data, owner_errors = owner_schema.load(ori, session=s)

            # assert we can NOT save it
            with pytest.raises(Exception):
                owner_data.save(session=s)

