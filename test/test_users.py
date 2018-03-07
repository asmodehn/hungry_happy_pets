import unittest
import json

from hypothesis import given
import hypothesis.strategies as st

try:
    from .utils import clean_app_test_client
except SystemError:
    from utils import clean_app_test_client

from app.users import user_schema


# BROWSE
# CAREFUL : See : https://github.com/pytest-dev/pytest/issues/916
@given(st.lists(elements=st.fixed_dictionaries({'nick': st.text(), 'email': st.text()})))
def test_api_can_get_users(dict_list):
    """Test API can get a user (GET request)."""

    # binds the app to the current context
    with clean_app_test_client(config_name="testing") as client:

        for d in dict_list:

            # generating a user from hypothesis data via marshmallow
            user_loaded = user_schema.load({'nick': d.get('nick'), 'email': d.get('email')})
            user = user_loaded.data
            #print(user)

            # writing to DB
            user.save()

        result = client.get('/api/users/')
        assert result.status_code == 200
        test_data = json.loads(result.data.decode('utf-8'))

        assert len(test_data) == len(dict_list)
        for u in test_data:
            assert {'nick': u.get('nick'), 'email': u.get('email')} in [{'nick': d.get('nick'), 'email': d.get('email').lower()} for d in dict_list]

        for d in dict_list:
            assert {k: v.lower() if k == 'email' else v for k, v in d.items()} in [{'nick': t.get('nick'), 'email': t.get('email')} for t in test_data]


# READ
@given(nick=st.text(), email=st.text())
def test_api_can_get_user_by_id(nick, email):
    """Test API can get a single user by using it's id."""
    # binds the app to the current context
    with clean_app_test_client(config_name="testing") as client:
        # Generate a random user test model in DB
        # user = mixer.blend(User, nick='testuser', email='tester@comp.any')

        # generating a user from hypothesis data via marshmallow
        user_loaded = user_schema.load({'nick': nick, 'email': email})
        user = user_loaded.data
        #print(user)

        # writing to DB
        user.save()

        result = client.get('/api/users/{}'.format(user.id))
        assert result.status_code == 200
        test_data = json.loads(result.data.decode('utf-8'))
        assert test_data.get('nick') == user.nick
        assert test_data.get('email') == user.email
        #print(test_data)


# EDIT
@given(nick=st.text(), email=st.text(), new_email=st.text())
def test_user_email_can_be_edited(nick, email, new_email):
    """Test API can edit an existing user. (PUT request)"""

    # binds the app to the current context
    with clean_app_test_client(config_name="testing") as client:

        # generating a user from hypothesis data via marshmallow
        user_loaded = user_schema.load({'nick': nick, 'email': email})
        user = user_loaded.data
        # print(user)

        # writing to DB
        user.save()

        result = client.put(
            '/api/users/{}'.format(user.id),
            headers={'Content-Type': 'application/json'},
            data=json.dumps({"email": new_email})
        )
        assert result.status_code == 200
        test_data = json.loads(result.data.decode('utf-8'))
        assert test_data.get('nick') == user.nick
        assert test_data.get('email') == new_email
        # print(test_data)

        # another request to insure persistence
        result = client.get('/api/users/{}'.format(user.id))
        assert result.status_code == 200
        test_data = json.loads(result.data.decode('utf-8'))
        assert test_data.get('nick') == user.nick
        assert test_data.get('email') == new_email

# TODO : More edits (check if allowed or not)


# ADD
@given(nick=st.text(), email=st.text())
def test_user_creation(nick, email):
    """Test API can create a user (POST request)"""

    with clean_app_test_client(config_name="testing") as client:
        res = client.post(
            '/api/users/',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({'nick': nick, 'email': email}))
        assert res.status_code == 201
        new_user = json.loads(res.data.decode('utf-8'))

        # consecutive request with id
        result = client.get('/api/users/{}'.format(new_user.get('id')))
        assert result.status_code == 200
        test_data = json.loads(result.data.decode('utf-8'))
        assert test_data.get('nick') == new_user.get('nick')
        assert test_data.get('email') == new_user.get('email')


# DELETE
@given(nick=st.text(), email=st.text())
def test_user_deletion(nick, email):
    """Test API can delete an existing user. (DELETE request)."""

    # binds the app to the current context
    with clean_app_test_client(config_name="testing") as client:
        # generating a user from hypothesis data via marshmallow
        user_loaded = user_schema.load({'nick': nick, 'email': email})
        user = user_loaded.data
        # print(user)

        # writing to DB
        user.save()

        res = client.delete('/api/users/{}'.format(user.id))
        assert res.status_code == 204

        # Test to see if it exists, should return a 404
        result = client.get('/api/users/{}'.format(user.id))
        assert result.status_code == 404


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
