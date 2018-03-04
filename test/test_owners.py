import unittest
import os
import json

from mixer.backend.sqlalchemy import TypeMixer
from mixer.backend.flask import mixer


from app.owners import Owner, owner_schema
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


class OwnerTestCase(unittest.TestCase):
    """This class handles test for owners"""

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

    def test_api_can_get_owners(self):
        """Test API can get a user (GET request)."""

        # binds the app to the current context
        with self.app.app_context():
            # Generate 10 random user test model in DB
            test_models = mixer.cycle(10).blend(Owner, nick=mixer.RANDOM, email=mixer.RANDOM)

            result = self.client().get('/api/owners/')
            self.assertEqual(result.status_code, 200)
            test_data = json.loads(result.data.decode('utf-8'))

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

    def test_api_can_get_user_by_id(self):
        """Test API can get a single user by using it's id."""
        # binds the app to the current context
        with self.app.app_context():
            # Generate a random user test model in DB
            test_model = mixer.blend(Owner, nick='testuser', email='tester@comp.any')

            result = self.client().get('/api/owners/{}'.format(test_model.id))
            self.assertEqual(result.status_code, 200)
            test_data = json.loads(result.data.decode('utf-8'))
            self.assertEqual(test_data.get('nick'), test_model.nick)
            self.assertEqual(test_data.get('email'), test_model.email)
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
