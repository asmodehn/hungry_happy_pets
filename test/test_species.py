import unittest
import os
import json

from hypothesis import given
import hypothesis.strategies as st

try:
    from .utils import clean_app_test_client
except SystemError:
    from utils import clean_app_test_client

from app.species import species_schema


# BROWSE
# See : https://github.com/pytest-dev/pytest/issues/916
@given(names=st.lists(st.text(), unique=True), data=st.data())
def test_api_can_get_species(names, data):
    """Test API can get a user (GET request)."""

    # binds the app to the current context
    with clean_app_test_client(config_name="testing") as client:

        dict_list = []

        for name in names:
            # SQL INTEGER range
            happy_rate = data.draw(st.integers(min_value=-2147483648, max_value=2147483647), label='happy_rate')
            hunger_rate = data.draw(st.integers(min_value=-2147483648, max_value=2147483647), label='hunger_rate')

            # building local dict to compare later
            dict_list.append({'name': name, 'happy_rate': happy_rate, 'hunger_rate': hunger_rate})

            # generating a species from hypothesis data via marshmallow
            species_loaded = species_schema.load({'name': name, 'happy_rate': happy_rate, 'hunger_rate': hunger_rate})
            species = species_loaded.data
            #print(species)

            # writing to DB
            species.save()

        result = client.get('/api/species/')
        assert result.status_code == 200
        test_data = json.loads(result.data.decode('utf-8'))

        assert len(test_data) == len(dict_list)
        for u in test_data:
            assert {'name': u.get('name'), 'happy_rate': u.get('happy_rate'), 'hunger_rate': u.get('hunger_rate')} in dict_list

        for d in dict_list:
            assert d in [{'name': t.get('name'), 'happy_rate': t.get('happy_rate'), 'hunger_rate': t.get('hunger_rate')} for t in test_data]

# READ
@given(
    name=st.text(),
    happy_rate=st.integers(min_value=-2147483648, max_value=2147483647),
    hunger_rate=st.integers(min_value=-2147483648, max_value=2147483647)
)
def test_api_can_get_species_by_id(name, happy_rate, hunger_rate):
    """Test API can get a single species by using it's id."""
    # binds the app to the current context
    with clean_app_test_client(config_name="testing") as client:
        # generating a species from hypothesis data via marshmallow
        species_loaded = species_schema.load({'name': name, 'happy_rate': happy_rate, 'hunger_rate': hunger_rate})
        species = species_loaded.data
        #print(species)

        # writing to DB
        species.save()

        result = client.get('/api/species/{}'.format(species.id))
        assert result.status_code == 200
        test_data = json.loads(result.data.decode('utf-8'))
        assert test_data.get('name') == species.name
        assert test_data.get('happy_rate') == species.happy_rate
        assert test_data.get('hunger_rate') == species.hunger_rate
        #print(test_data)

# EDIT
@given(name=st.text(),
       happy_rate=st.integers(min_value=-2147483648, max_value=2147483647),
       hunger_rate=st.integers(min_value=-2147483648, max_value=2147483647),
       new_hunger_rate=st.integers(min_value=-2147483648, max_value=2147483647))
def test_species_hunger_can_be_edited(name, happy_rate, hunger_rate, new_hunger_rate):
    """Test API can edit an existing species. (PUT request)"""

    # binds the app to the current context
    with clean_app_test_client(config_name="testing") as client:

        # generating a species from hypothesis data via marshmallow
        species_loaded = species_schema.load({'name': name, 'happy_rate': happy_rate, 'hunger_rate': hunger_rate})
        species = species_loaded.data
        # print(species)

        # writing to DB
        species.save()

        result = client.put(
            '/api/species/{}'.format(species.id),
            headers={'Content-Type': 'application/json'},
            data=json.dumps({"hunger_rate": new_hunger_rate})
        )
        assert result.status_code == 200
        test_data = json.loads(result.data.decode('utf-8'))
        assert test_data.get('name') == species.name
        assert test_data.get('happy_rate') == species.happy_rate
        assert test_data.get('hunger_rate') == new_hunger_rate
        # print(test_data)

        # another request to insure persistence
        result = client.get('/api/species/{}'.format(species.id))
        assert result.status_code == 200
        test_data = json.loads(result.data.decode('utf-8'))
        assert test_data.get('name') == species.name
        assert test_data.get('happy_rate') == species.happy_rate
        assert test_data.get('hunger_rate') == new_hunger_rate

# TODO : More edits (check if allowed or not)


# ADD
@given(name=st.text(),
       happy_rate=st.integers(min_value=-2147483648, max_value=2147483647),
       hunger_rate=st.integers(min_value=-2147483648, max_value=2147483647))
def test_species_creation(name, happy_rate, hunger_rate):
    """Test API can create a species (POST request)"""

    # binds the app to the current context
    with clean_app_test_client(config_name="testing") as client:
        res = client.post(
            '/api/species/',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({'name': name, 'happy_rate': happy_rate, 'hunger_rate': hunger_rate}))
        assert res.status_code == 201
        new_species = json.loads(res.data.decode('utf-8'))

        # consecutive request with id
        result = client.get('/api/species/{}'.format(new_species.get('id')))
        assert result.status_code == 200
        test_data = json.loads(result.data.decode('utf-8'))
        assert test_data.get('name') == new_species.get('name')
        assert test_data.get('happy_rate') == new_species.get('happy_rate')
        assert test_data.get('hunger_rate') == new_species.get('hunger_rate')


# DELETE
@given(name=st.text(), happy_rate=st.integers(min_value=-2147483648, max_value=2147483647), hunger_rate=st.integers(min_value=-2147483648, max_value=2147483647))
def test_species_deletion(name, happy_rate, hunger_rate):
    """Test API can delete an existing species. (DELETE request)."""

    # binds the app to the current context
    with clean_app_test_client(config_name="testing") as client:
        # generating a species from hypothesis data via marshmallow
        species_loaded = species_schema.load({'name': name, 'happy_rate': happy_rate, 'hunger_rate': hunger_rate})
        species = species_loaded.data
        # print(species)

        # writing to DB
        species.save()

        res = client.delete('/api/species/{}'.format(species.id))
        assert res.status_code == 204

        # Test to see if it exists, should return a 404
        result = client.get('/api/species/{}'.format(species.id))
        assert result.status_code == 404




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
