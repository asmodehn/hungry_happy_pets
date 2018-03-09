import unittest
import os
import json

from hypothesis import given
import hypothesis.strategies as st

try:
    from .utils import clean_app_test_client, dummy_owner, dummy_species
except SystemError:
    from utils import clean_app_test_client, dummy_owner, dummy_species

from app.animals import models, animal_schema


# BROWSE
@given(names=st.lists(st.text()), data=st.data())
def test_api_can_get_animals(names, data):
    """Test API can get a user (GET request)."""

    # binds the app to the current context
    with clean_app_test_client(config_name="testing") as client:

        with dummy_owner() as owner:

            with dummy_species() as species:

                dict_list = []
                animal_list = []
                for name in names:
                    # SQL INTEGER range
                    happy = data.draw(st.integers(min_value=-2147483648, max_value=2147483647), label='happy')
                    hungry = data.draw(st.integers(min_value=-2147483648, max_value=2147483647), label='hungry')

                    # building local dict to compare later
                    dict_list.append({'name': name, 'happy': happy, 'hungry': hungry})

                    # generating a species from hypothesis data via marshmallow
                    animal_loaded = animal_schema.load({
                        'name': name,
                        'happy': happy,
                        'hungry': hungry,
                        'species_id': species.get('id'),
                        'owner_id': owner.get('id'),
                    })
                    animal = animal_loaded.data
                    # print(species)

                    # writing to DB
                    animal.save()

                    animal_list.append(animal)

                result = client.get('/api/animals/')
                assert result.status_code == 200
                test_data = json.loads(result.data.decode('utf-8'))

                assert len(test_data) == len(dict_list)
                for u in test_data:
                    assert {'name': u.get('name'), 'happy': u.get('happy'),
                            'hungry': u.get('hungry')} in dict_list

                for d in dict_list:
                    assert d in [{'name': t.get('name'), 'happy': t.get('happy'), 'hungry': t.get('hungry')}
                                 for t in test_data]

                for a in animal_list:
                    # deleting animal before dropping species
                    a.delete()


# READ
@given(name=st.text(), data=st.data())
def test_api_can_get_animal_by_id(name, data):
    """Test API can get a single owner by using it's id."""
    # binds the app to the current context
    with clean_app_test_client(config_name="testing") as client:

        with dummy_owner() as owner:

            with dummy_species() as species:

                # SQL INTEGER range
                happy = data.draw(st.integers(min_value=-2147483648, max_value=2147483647), label='happy')
                hungry = data.draw(st.integers(min_value=-2147483648, max_value=2147483647), label='hungry')

                # generating an animal from hypothesis data via marshmallow
                animal_loaded = animal_schema.load({
                    'name': name,
                    'happy': happy,
                    'hungry': hungry,
                    'species_id': species.get('id'),
                    'owner_id': owner.get('id'),
                })
                animal = animal_loaded.data

                # writing to DB
                animal.save()

                result = client.get('/api/animals/{}'.format(animal.id))
                assert result.status_code == 200
                test_data = json.loads(result.data.decode('utf-8'))
                assert test_data.get('name') == animal.name
                assert test_data.get('happy') == animal.happy
                assert test_data.get('hungry') == animal.hungry

                # deleting from db before dropping required species
                animal.delete()
#
#
# # EDIT
# @given(nick=st.text(), email=st.text(), new_email=st.text())
# def test_owner_email_can_be_edited(nick, email, new_email):
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
#
# # TODO : More edits (check if allowed or not)


# ADD
@given(name=st.text(), happy=st.integers(min_value=-2147483648, max_value=2147483647), hungry=st.integers(min_value=-2147483648, max_value=2147483647))
def test_animal_creation(name, happy, hungry):
    """Test API can create a user (POST request)"""
    # binds the app to the current context
    with clean_app_test_client(config_name="testing") as client:

        with dummy_owner() as owner:

            with dummy_species() as species:

                res = client.post(
                    '/api/animals/',
                    headers={'Content-Type': 'application/json'},
                    data=json.dumps({'name': name, 'happy': happy, 'hungry': hungry, 'species_id': species.get('id'), 'owner_id': owner.get('id')}))
                assert res.status_code == 201
                new_animal = json.loads(res.data.decode('utf-8'))

                # consecutive request with id
                result = client.get('/api/animals/{}'.format(new_animal.get('id')))
                assert result.status_code == 200
                test_data = json.loads(result.data.decode('utf-8'))
                assert test_data.get('name') == name
                assert test_data.get('happy') == happy
                assert test_data.get('hungry') == hungry

                # deleting animal before dropping species
                animal_loaded, animal_errors = animal_schema.load(test_data)
                animal_loaded.delete()


# DELETE
@given(name=st.text(), happy=st.integers(min_value=-2147483648, max_value=2147483647), hungry=st.integers(min_value=-2147483648, max_value=2147483647))
def test_animal_deletion(name, happy, hungry):
    """Test API can delete an existing user. (DELETE request)."""

    # binds the app to the current context
    with clean_app_test_client(config_name="testing") as client:

        with dummy_owner() as owner:

            with dummy_species() as species:

                # generating a user from hypothesis data via marshmallow
                animal_loaded = animal_schema.load({'name': name, 'happy': happy, 'hungry': hungry, 'species_id': species.get('id'), 'owner_id': owner.get('id')})
                animal = animal_loaded.data
                # print(user)

                # writing to DB
                animal.save()

                res = client.delete('/api/animals/{}'.format(animal.id))
                assert 204 == res.status_code

                # Test to see if it exists, should return a 404
                result = client.get('/api/animals/{}'.format(animal.id))
                assert 404 == result.status_code


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

