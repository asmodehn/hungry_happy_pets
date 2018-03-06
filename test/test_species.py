import unittest
import os
import json

from hypothesis import given
import hypothesis.strategies as st

from app.species import Species, species_schema
from app import create_app, db



class SpeciesTestCase(unittest.TestCase):
    """This class represents the species test case. We follow here the BREAD model"""

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
    @given(st.lists(elements=st.fixed_dictionaries({
        'name': st.text(),
        'happy_rate': st.integers(min_value=-2147483648, max_value=2147483647),  # SQL INTEGER range
        'hunger_rate': st.integers(min_value=-2147483648, max_value=2147483647)  # SQL INTEGER range
    })))
    def test_api_can_get_species(self, dict_list):
        """Test API can get a user (GET request)."""

        # binds the app to the current context
        with self.app.app_context():

            for d in dict_list:

                # generating a species from hypothesis data via marshmallow
                species_loaded = species_schema.load({'name': d.get('name'), 'happy_rate': d.get('happy_rate'), 'hunger_rate': d.get('hunger_rate')})
                species = species_loaded.data
                #print(species)

                # writing to DB
                species.save()

            result = self.client().get('/api/species/')
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
            #             d = species_schema.jsonify(m)
            #     self.assertIn(d, test_data)
            #
            # # to make sure we didnt create any extra data
            # for d in test_data:
            #     m = species_schema.load(d)
            #     self.assertIn(m, test_models)

    # READ
    @given(
        name=st.text(),
        happy_rate=st.integers(min_value=-2147483648, max_value=2147483647),
        hunger_rate=st.integers(min_value=-2147483648, max_value=2147483647)
    )
    def test_api_can_get_species_by_id(self, name, happy_rate, hunger_rate):
        """Test API can get a single species by using it's id."""
        # binds the app to the current context
        with self.app.app_context():
            # generating a species from hypothesis data via marshmallow
            species_loaded = species_schema.load({'name': name, 'happy_rate': happy_rate, 'hunger_rate': hunger_rate})
            species = species_loaded.data
            #print(species)

            # writing to DB
            species.save()

            result = self.client().get('/api/species/{}'.format(species.id))
            self.assertEqual(result.status_code, 200)
            test_data = json.loads(result.data.decode('utf-8'))
            self.assertEqual(test_data.get('name'), species.name)
            self.assertEqual(test_data.get('happy_rate'), species.happy_rate)
            self.assertEqual(test_data.get('hunger_rate'), species.hunger_rate)
            #print(test_data)

    # EDIT
    @given(name=st.text(),
           happy_rate=st.integers(min_value=-2147483648, max_value=2147483647),
           hunger_rate=st.integers(min_value=-2147483648, max_value=2147483647),
           new_hunger_rate=st.integers(min_value=-2147483648, max_value=2147483647))
    def test_species_hunger_can_be_edited(self, name, happy_rate, hunger_rate, new_hunger_rate):
        """Test API can edit an existing species. (PUT request)"""

        # binds the app to the current context
        with self.app.app_context():

            # generating a species from hypothesis data via marshmallow
            species_loaded = species_schema.load({'name': name, 'happy_rate': happy_rate, 'hunger_rate': hunger_rate})
            species = species_loaded.data
            # print(species)

            # writing to DB
            species.save()

            result = self.client().put(
                '/api/species/{}'.format(species.id),
                headers={'Content-Type': 'application/json'},
                data=json.dumps({"hunger_rate": new_hunger_rate})
            )
            self.assertEqual(result.status_code, 200)
            test_data = json.loads(result.data.decode('utf-8'))
            self.assertEqual(test_data.get('name'), species.name)
            self.assertEqual(test_data.get('happy_rate'), species.happy_rate)
            self.assertEqual(test_data.get('hunger_rate'), new_hunger_rate)
            # print(test_data)

            # another request to insure persistence
            result = self.client().get('/api/species/{}'.format(species.id))
            self.assertEqual(result.status_code, 200)
            test_data = json.loads(result.data.decode('utf-8'))
            self.assertEqual(test_data.get('name'), species.name)
            self.assertEqual(test_data.get('happy_rate'), species.happy_rate)
            self.assertEqual(test_data.get('hunger_rate'), new_hunger_rate)

    # TODO : More edits (check if allowed or not)

    # ADD
    @given(name=st.text(),
           happy_rate=st.integers(min_value=-2147483648, max_value=2147483647),
           hunger_rate=st.integers(min_value=-2147483648, max_value=2147483647))
    def test_species_creation(self, name, happy_rate, hunger_rate):
        """Test API can create a species (POST request)"""

        res = self.client().post(
            '/api/species/',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({'name': name, 'happy_rate': happy_rate, 'hunger_rate': hunger_rate}))
        self.assertEqual(res.status_code, 201)
        new_species = json.loads(res.data.decode('utf-8'))

        # consecutive request with id
        result = self.client().get('/api/species/{}'.format(new_species.get('id')))
        self.assertEqual(result.status_code, 200)
        test_data = json.loads(result.data.decode('utf-8'))
        self.assertEqual(test_data.get('name'), new_species.get('name'))
        self.assertEqual(test_data.get('happy_rate'), new_species.get('happy_rate'))
        self.assertEqual(test_data.get('hunger_rate'), new_species.get('hunger_rate'))

    # DELETE
    @given(name=st.text(), happy_rate=st.integers(min_value=-2147483648, max_value=2147483647), hunger_rate=st.integers(min_value=-2147483648, max_value=2147483647))
    def test_species_deletion(self, name, happy_rate, hunger_rate):
        """Test API can delete an existing species. (DELETE request)."""

        # binds the app to the current context
        with self.app.app_context():
            # generating a species from hypothesis data via marshmallow
            species_loaded = species_schema.load({'name': name, 'happy_rate': happy_rate, 'hunger_rate': hunger_rate})
            species = species_loaded.data
            # print(species)

            # writing to DB
            species.save()

            res = self.client().delete('/api/species/{}'.format(species.id))
            self.assertEqual(res.status_code, 204)

            # Test to see if it exists, should return a 404
            result = self.client().get('/api/species/{}'.format(species.id))
            self.assertEqual(result.status_code, 404)




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
