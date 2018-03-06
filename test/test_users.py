import unittest
import os
import json

from hypothesis import given
import hypothesis.strategies as st


from app.users import User, user_schema
from app import create_app, db



class UserTestCase(unittest.TestCase):
    """This class represents the user test case. We follow here the BREAD model"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            # drop all tables just in case
            db.session.remove()
            db.drop_all()
            # create all tables
            db.create_all()

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    # BROWSE
    # See : https://github.com/pytest-dev/pytest/issues/916
    @given(st.lists(elements=st.fixed_dictionaries({'nick': st.text(), 'email': st.text()})))
    def test_api_can_get_users(self, dict_list):
        """Test API can get a user (GET request)."""

        # binds the app to the current context
        with self.app.app_context():

            for d in dict_list:

                # generating a user from hypothesis data via marshmallow
                user_loaded = user_schema.load({'nick': d.get('nick'), 'email': d.get('email')})
                user = user_loaded.data
                #print(user)

                # writing to DB
                user.save()

            result = self.client().get('/api/users/')
            self.assertEqual(result.status_code, 200)
            test_data = json.loads(result.data.decode('utf-8'))

            self.assertEqual(len(test_data), len(dict_list))
            for u in test_data:
                self.assertIn(u, dict_list)

            for d in dict_list:
                self.assertIn(d, test_data)

            #print(test_data)

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

    # READ
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

    # EDIT
    @given(nick=st.text(), email=st.text(), new_email=st.text())
    def test_user_email_can_be_edited(self, nick, email, new_email):
        """Test API can edit an existing user. (PUT request)"""

        # binds the app to the current context
        with self.app.app_context():

            # generating a user from hypothesis data via marshmallow
            user_loaded = user_schema.load({'nick': nick, 'email': email})
            user = user_loaded.data
            # print(user)

            # writing to DB
            user.save()

            result = self.client().put(
                '/api/users/{}'.format(user.id),
                headers={'Content-Type': 'application/json'},
                data=json.dumps({"email": new_email})
            )
            self.assertEqual(result.status_code, 200)
            test_data = json.loads(result.data.decode('utf-8'))
            self.assertEqual(test_data.get('nick'), user.nick)
            self.assertEqual(test_data.get('email'), new_email)
            # print(test_data)

            # another request to insure persistence
            result = self.client().get('/api/users/{}'.format(user.id))
            self.assertEqual(result.status_code, 200)
            test_data = json.loads(result.data.decode('utf-8'))
            self.assertEqual(test_data.get('nick'), user.nick)
            self.assertEqual(test_data.get('email'), new_email)

    # TODO : More edits (check if allowed or not)

    # ADD
    @given(nick=st.text(), email=st.text())
    def test_user_creation(self, nick, email):
        """Test API can create a user (POST request)"""

        res = self.client().post(
            '/api/users/',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({'nick': nick, 'email': email}))
        self.assertEqual(res.status_code, 201)
        new_user = json.loads(res.data.decode('utf-8'))

        # consecutive request with id
        result = self.client().get('/api/users/{}'.format(new_user.get('id')))
        self.assertEqual(result.status_code, 200)
        test_data = json.loads(result.data.decode('utf-8'))
        self.assertEqual(test_data.get('nick'), new_user.get('nick'))
        self.assertEqual(test_data.get('email'), new_user.get('email'))

    # DELETE
    @given(nick=st.text(), email=st.text())
    def test_user_deletion(self, nick, email):
        """Test API can delete an existing user. (DELETE request)."""

        # binds the app to the current context
        with self.app.app_context():
            # generating a user from hypothesis data via marshmallow
            user_loaded = user_schema.load({'nick': nick, 'email': email})
            user = user_loaded.data
            # print(user)

            # writing to DB
            user.save()

            res = self.client().delete('/api/users/{}'.format(user.id))
            self.assertEqual(res.status_code, 204)

            # Test to see if it exists, should return a 404
            result = self.client().get('/api/users/{}'.format(user.id))
            self.assertEqual(result.status_code, 404)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
