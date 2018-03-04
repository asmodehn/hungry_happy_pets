import unittest
import os
import json

from hypothesis import given
import hypothesis.strategies as st

from mixer.backend.sqlalchemy import TypeMixer
from mixer.backend.flask import mixer


from app.users import User, user_schema
from app import create_app, db



# class UserTypeMixer(TypeMixer):
#
#     def __init__(self, cls, **params):
#         super(UserTypeMixer, self).__init__(cls, **params)
#
#     def populate_target(self, values):
#         target = self.__scheme(**values)
#         return target
#
# mixer.type_mixer_cls = UserTypeMixer


class UserTestCase(unittest.TestCase):
    """This class represents the user test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        mixer.init_app(self.app)

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()


    # def test_bucketlist_creation(self):
    #     """Test API can create a user (POST request)"""
    #     res = self.client().post('/users/', data=self.user)
    #     self.assertEqual(res.status_code, 201)
    #     self.assertIn('Go to Borabora', str(res.data))

    @given(nick=st.text(), email=st.text())
    def test_api_can_get_users(self, nick, email):
        """Test API can get a user (GET request)."""

        # binds the app to the current context
        with self.app.app_context():
            # Generate 10 random user test model in DB
            # test_models = mixer.cycle(10).blend(User, nick=mixer.RANDOM, email=mixer.RANDOM)

            # generating a user from hypothesis data via marshmallow
            user_loaded = user_schema.load({'nick': nick, 'email': email})
            user = user_loaded.data
            print(user)

            # writing to DB
            user.save()

            result = self.client().get('/api/users/')
            self.assertEqual(result.status_code, 200)
            test_data = json.loads(result.data.decode('utf-8'))

            print(test_data)

            # TODO assert
            # for m in test_models:
            #     for d in test_data:
            #         for k,v  in d.items():
            #             self.assertEqual(getattr(m, k), v)
            #             d = user_schema.jsonify(m)
            #     self.assertIn(d, test_data)
            #
            # # to make sure we didnt create any extra data
            # for d in test_data:
            #     m = user_schema.load(d)
            #     self.assertIn(m, test_models)

    @given(nick=st.text(), email=st.text())
    def test_api_can_get_user_by_id(self, nick, email):
        """Test API can get a single user by using it's id."""
        # binds the app to the current context
        with self.app.app_context():
            # Generate a random user test model in DB
            # user = mixer.blend(User, nick='testuser', email='tester@comp.any')

            # generating a user from hypothesis data via marshmallow
            user_loaded = user_schema.load({'nick': nick, 'email': email})
            user = user_loaded.data
            #print(user)

            # writing to DB
            user.save()

            result = self.client().get('/api/users/{}'.format(user.id))
            self.assertEqual(result.status_code, 200)
            test_data = json.loads(result.data.decode('utf-8'))
            self.assertEqual(test_data.get('nick'), user.nick)
            self.assertEqual(test_data.get('email'), user.email)
            #print(test_data)


    #
    # def test_bucketlist_can_be_edited(self):
    #     """Test API can edit an existing bucketlist. (PUT request)"""
    #     rv = self.client().post(
    #         '/bucketlists/',
    #         data={'name': 'Eat, pray and love'})
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.client().put(
    #         '/bucketlists/1',
    #         data={
    #             "name": "Dont just eat, but also pray and love :-)"
    #         })
    #     self.assertEqual(rv.status_code, 200)
    #     results = self.client().get('/bucketlists/1')
    #     self.assertIn('Dont just eat', str(results.data))
    #
    # def test_bucketlist_deletion(self):
    #     """Test API can delete an existing bucketlist. (DELETE request)."""
    #     rv = self.client().post(
    #         '/bucketlists/',
    #         data={'name': 'Eat, pray and love'})
    #     self.assertEqual(rv.status_code, 201)
    #     res = self.client().delete('/bucketlists/1')
    #     self.assertEqual(res.status_code, 200)
    #     # Test to see if it exists, should return a 404
    #     result = self.client().get('/bucketlists/1')
    #     self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
