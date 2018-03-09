import unittest
import os
import json


from hypothesis import given
import hypothesis.strategies as st

try:
    from .utils import clean_app_test_client, dummy_user, dummy_user_list
except SystemError:
    from utils import clean_app_test_client, dummy_user, dummy_user_list

from app.owners import models, owner_schema



# BROWSE
@st.composite
def zip_strat(draw, st1, st2):
    # we need to draw separately (useful to guarantee some properties - like uniqueness)
    list1 = draw(st1)
    list2 = draw(st2)
    # and zip it
    return zip(list1, list2)


@given(nicks_emails=zip_strat(st.lists(st.text(), unique=True), st.lists(st.text(), unique=True)))
def test_api_can_get_owners(nicks_emails):
    """Test API can get a user (GET request)."""

    # binds the app to the current context
    with clean_app_test_client(config_name="testing") as client:

        with dummy_user_list(nicks_emails) as user_list:

            own_list = []
            for user in user_list:

                # generating its owner
                owner_loaded = owner_schema.load({'user_id': user.get('id')})
                owner = owner_loaded.data
                # print(owner)

                # writing to DB
                owner.save()

                own_list.append(owner)

            result = client.get('/api/owners/')
            assert result.status_code == 200
            test_data = json.loads(result.data.decode('utf-8'))

            assert len(test_data) == len(user_list)
            for u in test_data:
                assert u.get('user') in user_list

            for d in user_list:
                assert d in [t.get('user') for t in test_data]

            for o in own_list:
                # deleting owner before dropping user
                o.delete()


# READ
@given(nick=st.text(), email=st.text())
def test_api_can_get_owner_by_id(nick, email):
    """Test API can get a single owner by using it's id."""
    # binds the app to the current context
    with clean_app_test_client(config_name="testing") as client:

        with dummy_user(nick='testuser', email='tester@comp.any') as user:

            # generating its owner
            owner_loaded = owner_schema.load({'user_id': user.get('id')})
            owner = owner_loaded.data
            #print(owner)

            # writing to DB
            owner.save()

            result = client.get('/api/owners/{}'.format(owner.id))
            assert result.status_code == 200
            test_data = json.loads(result.data.decode('utf-8'))
            # checking populated user data
            assert test_data.get('user') == user
            # checking populated pets data
            assert test_data.get('pets') == None  #or [] ??

            # deleting owner before dropping user
            owner.delete()

            #print(test_data)

# # EDIT
# @given(nick=st.text(), email=st.text(), new_email=st.text())
# def test_owner_pets_can_be_edited(nick, email, new_email):
#     """Test API can edit an existing owner. (PUT request)"""
#
#     # binds the app to the current context
#     with clean_app_test_client(config_name="testing") as client:
#
#         # generating a user from hypothesis data via marshmallow
#         user_loaded = owner_schema.load({'nick': nick, 'email': email})
#         user = user_loaded.data
#         # print(user)
#
#         # writing to DB
#         user.save()
#
#         result = client.put(
#             '/api/owners/{}'.format(user.id),
#             headers={'Content-Type': 'application/json'},
#             data=json.dumps({"email": new_email})
#         )
#         assert result.status_code == 200
#         test_data = json.loads(result.data.decode('utf-8'))
#         assert test_data.get('nick') == user.nick
#         assert test_data.get('email') == new_email
#         # print(test_data)
#
#         # another request to insure persistence
#         result = client.get('/api/owners/{}'.format(user.id))
#         assert result.status_code == 200
#         test_data = json.loads(result.data.decode('utf-8'))
#         assert test_data.get('nick') == user.nick
#         assert test_data.get('email') == new_email

# TODO : More edits (check if allowed or not)


# ADD
@given(nick=st.text(), email=st.text())
def test_owner_creation(nick, email):
    """Test API can create a user (POST request)"""
    # binds the app to the current context
    with clean_app_test_client(config_name="testing") as client:

        with dummy_user(nick='testuser', email='tester@comp.any') as user:

            res = client.post(
                '/api/owners/',
                headers={'Content-Type': 'application/json'},
                data=json.dumps({'user_id': user.get('id')}))
            assert res.status_code == 201
            new_owner = json.loads(res.data.decode('utf-8'))

            # consecutive request with id
            result = client.get('/api/owners/{}'.format(new_owner.get('id')))
            assert result.status_code == 200
            test_data = json.loads(result.data.decode('utf-8'))
            assert user == test_data.get('user')
            assert None == test_data.get('pets')

            # deleting owner before dropping user
            owner_loaded, owner_errors = owner_schema.load(test_data)
            owner_loaded.delete()


# DELETE
@given(nick=st.text(), email=st.text())
def test_owner_deletion(nick, email):
    """Test API can delete an existing user. (DELETE request)."""

    # binds the app to the current context
    with clean_app_test_client(config_name="testing") as client:

        with dummy_user(nick=nick, email=email) as user:

            # generating a owner from hypothesis data via marshmallow
            owner_loaded = owner_schema.load({'user_id': user.get('id')})
            owner = owner_loaded.data

            # writing to DB
            owner.save()

            res = client.delete('/api/owners/{}'.format(user.get('id')))
            assert res.status_code == 204

            # Test to see if it exists, should return a 404
            result = client.get('/api/owners/{}'.format(user.get('id')))
            assert result.status_code == 404

            # finally we can delete the user


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
