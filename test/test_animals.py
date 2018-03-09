import unittest
import os
import json

from hypothesis import given
import hypothesis.strategies as st

try:
    from .utils import clean_app_test_client
except SystemError:
    from utils import clean_app_test_client



# BROWSE
@given(names=st.lists(st.text()), data=st.data())
def test_api_can_get_animals(names, data):
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
            animal_loaded = animals_schema.load({'name': name, 'happy_rate': happy_rate, 'hunger_rate': hunger_rate})
            animal = animal_loaded.data
            # print(species)

            # writing to DB
            animal.save()

        result = client.get('/api/animals/')
        assert result.status_code == 200
        test_data = json.loads(result.data.decode('utf-8'))

        assert len(test_data) == len(dict_list)
        for u in test_data:
            assert {'name': u.get('name'), 'happy_rate': u.get('happy_rate'),
                    'hunger_rate': u.get('hunger_rate')} in dict_list

        for d in dict_list:
            assert d in [{'name': t.get('name'), 'happy_rate': t.get('happy_rate'), 'hunger_rate': t.get('hunger_rate')}
                         for t in test_data]

# READ
@given(nick=st.text(), email=st.text())
def test_api_can_get_owner_by_id(nick, email):
    """Test API can get a single owner by using it's id."""
    # binds the app to the current context
    with clean_app_test_client(config_name="testing") as client:

        # generating a user from hypothesis data via marshmallow

        # generating its owner
        owner_loaded = owner_schema.load(user={'nick': nick, 'email': email})
        owner = owner_loaded.data
        #print(owner)

        # writing to DB
        owner.save()

        result = client.get('/api/owners/{}'.format(owner.id))
        assert result.status_code == 200
        test_data = json.loads(result.data.decode('utf-8'))
        assert test_data.get('nick') == owner.nick
        assert test_data.get('email') == owner.email
        #print(test_data)

# EDIT
@given(nick=st.text(), email=st.text(), new_email=st.text())
def test_owner_email_can_be_edited(nick, email, new_email):
    """Test API can edit an existing owner. (PUT request)"""

    # binds the app to the current context
    with clean_app_test_client(config_name="testing") as client:

        # generating a user from hypothesis data via marshmallow
        user_loaded = owner_schema.load({'nick': nick, 'email': email})
        user = user_loaded.data
        # print(user)

        # writing to DB
        user.save()

        result = client.put(
            '/api/owners/{}'.format(user.id),
            headers={'Content-Type': 'application/json'},
            data=json.dumps({"email": new_email})
        )
        assert result.status_code == 200
        test_data = json.loads(result.data.decode('utf-8'))
        assert test_data.get('nick') == user.nick
        assert test_data.get('email') == new_email
        # print(test_data)

        # another request to insure persistence
        result = client.get('/api/owners/{}'.format(user.id))
        assert result.status_code == 200
        test_data = json.loads(result.data.decode('utf-8'))
        assert test_data.get('nick') == user.nick
        assert test_data.get('email') == new_email

# TODO : More edits (check if allowed or not)


# ADD
@given(nick=st.text(), email=st.text())
def test_owner_creation(nick, email):
    """Test API can create a user (POST request)"""
    # binds the app to the current context
    with clean_app_test_client(config_name="testing") as client:

        res = client.post(
            '/api/users/',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({'nick': nick, 'email': email}))
        assert res.status_code == 201
        new_user = json.loads(res.data.decode('utf-8'))

        # consecutive request with id
        result = client.get('/api/owners/{}'.format(new_user.get('id')))
        assert result.status_code == 200
        test_data = json.loads(result.data.decode('utf-8'))
        assert test_data.get('nick') == nick
        assert test_data.get('email') == email


# DELETE
@given(nick=st.text(), email=st.text())
def test_user_deletion(nick, email):
    """Test API can delete an existing user. (DELETE request)."""

    # binds the app to the current context
    with clean_app_test_client(config_name="testing") as client:

        # generating a user from hypothesis data via marshmallow
        user_loaded = owner_schema.load({'nick': nick, 'email': email})
        user = user_loaded.data
        # print(user)

        # writing to DB
        user.save()

        res = client.delete('/api/owners/{}'.format(user.id))
        assert res.status_code == 204

        # Test to see if it exists, should return a 404
        result = client.get('/api/owners/{}'.format(user.id))
        assert result.status_code == 404


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

