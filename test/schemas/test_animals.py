import unittest
import json

from hypothesis import given
import hypothesis.strategies as st

try:
    from .utils import clean_memorydb_session_from_schema
except SystemError:
    from utils import clean_memorydb_session_from_schema

from app.schemas import animal_schema, species_schema

def test_load_animals_species_id():

    with clean_memorydb_session_from_schema(animal_schema) as s:

        # load our dict
        animal_data, animal_errors = animal_schema.load({'name': 'testanimal', 'happy': 4, 'hungry': 42}, session=s)

        # check we canNOT save it
        animal_data.save(session=s)




#
#
# def dump_animals():
#
#
#
#     >>> import species, users, owners  #import other modules to resolve relationships
#     >>> Animal.metadata.create_all(engine)
#
#     >>> species_data, species_errors = species.species_schema.load({'name':'testspecies', 'happy_rate': 0.5, 'hunger_rate': 2.3}, session=session)
#     >>> species_data
#     <Species: testspecies>
#
#     >>> species_data.save(session=session)
#     >>> session.query(species.Species).all()
#     [<Species: testspecies>]
#
#     >>> animal_data = Animal(name='testanimal', happy=4, hungry=42)
#     >>> animal_data.species_id = species_data.id
#
#     >>> user_data, user_errors = users.user_schema.load({'nick': 'testuser', 'email': 'tester@comp.any'}, session=session)
#     >>> user_data
#     <User: testuser>
#
#     >>> user_data.save(session=session)
#     >>> session.query(users.User).all()
#     [<User: testuser>]
#
#     >>> owner_data, owner_errors = owners.owner_schema.load({}, session=session)
#     >>> owner_data
#     <Owner: None []>
#
#     >>> owner_data.user_id = user_data.id  # linking already existing user with its id
#     >>> owner_data.save(session=session) # validating relationship
#     >>> owner_data
#     <Owner: <User: testuser> []>
#
#     >>> animal_data.owner_id = owner_data.id
#     >>> animal_data.save(session=session)
#     >>> session.query(Animal).all()
#     [<Animal: testanimal <Species: testspecies>>]
#     >>> session.query(owners.Owner).all()
#     [<Owner: <User: testuser> [<Animal: testanimal <Species: testspecies>>]>]
#
#     >>> dump_data = animal_schema.dump(animal_data).data
#     >>> import pprint  #ordering dict output
#     >>> pprint.pprint(dump_data)  # doctest: +ELLIPSIS
#     {'happy': 4,
#      'hungry': 42,
#      'id': 1,
#      'name': 'testanimal',
#      'species': {'name': 'testspecies'}}
#
#     >>> animal_schema.load(dump_data, session=session).data
#     <Animal: testanimal <Species: testspecies>>