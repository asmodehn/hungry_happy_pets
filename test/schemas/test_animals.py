import unittest
import json

import pytest
from hypothesis import given
import hypothesis.strategies as st

try:
    from .utils import clean_memorydb_session_from_schema, dummy_species, dummy_owner
except SystemError:
    from utils import clean_memorydb_session_from_schema, dummy_species, dummy_owner

# import app.schemas import OwnerSchema  # used by animal indirect nested relation
from app.schemas import models, animal_schema, species_schema, owner_schema


@given(name=st.text(),
    happy=st.integers(min_value=-2147483648, max_value=2147483647),
    hungry=st.integers(min_value=-2147483648, max_value=2147483647)
)
def test_load_dump_animals_species_id_NO_owner_id_OK(name, happy, hungry):

    with clean_memorydb_session_from_schema(animal_schema) as s:

        with dummy_species(s) as species:

            ori = {'name': name, 'happy': happy, 'hungry': hungry, 'species_id': species.id}

            # load our dict
            animal_data, animal_errors = animal_schema.load(ori, session=s)

            # check we can save it
            animal_data.save(session=s)

            # retrieve it again
            animal_stored = s.query(models.Animal).get(animal_data.id)

            # compare models
            assert animal_stored == animal_data

            # serialize
            fin, err = animal_schema.dump(animal_stored)

            # pop the added id
            assert 'id' in fin
            fin.pop('id')

            # compare dicts
            # species_id should have been expanded to the dummy species
            # owner should be None
            assert fin.get('species') == species_schema.dump(species).data
            fin.pop('species')
            fin.pop('owner')
            # the rest should be identical
            ori.pop('species_id')
            assert fin == ori

            # deleting table before removing dummy species
            animal_stored.delete(session=s)


@given(name = st.text(),
    happy = st.integers(min_value=-2147483648, max_value=2147483647),
    hungry = st.integers(min_value=-2147483648, max_value=2147483647)
)
def test_load_dump_animals_species_id_owner_id_OK(name, happy, hungry):

    with clean_memorydb_session_from_schema(animal_schema) as s:

        with dummy_species(s) as species:

            with dummy_owner(s) as owner:

                ori = {'name': name, 'happy': happy, 'hungry': hungry, 'species_id': species.id, 'owner_id': owner.id}

                # load our dict
                animal_data, animal_errors = animal_schema.load(ori, session=s)

                # check we can save it
                animal_data.save(session=s)

                # retrieve it again
                animal_stored = s.query(models.Animal).get(animal_data.id)

                # compare models
                assert animal_stored == animal_data

                # serialize
                fin, err = animal_schema.dump(animal_stored)

                # pop the added id
                assert 'id' in fin
                fin.pop('id')

                # compare dicts
                # owner_id should have been expanded to the dummy owner
                assert fin.get('owner') == owner_schema.dump(owner).data

                # spcies_id should have been expanded to the dummy species
                assert fin.get('species') == species_schema.dump(species).data

                fin.pop('owner')
                fin.pop('species')
                # the rest should be identical
                ori.pop('owner_id')
                ori.pop('species_id')
                assert fin == ori

                # we should be able to delete the dummy owner but keep the orphan pet

            # retrieve it again
            animal_stored = s.query(models.Animal).get(animal_data.id)

            # serialize
            fin, err = animal_schema.dump(animal_stored)

            # pop the added id
            assert 'id' in fin
            fin.pop('id')

            assert fin.get('owner') is None

            # spcies_id should have been expanded to the dummy species
            assert fin.get('species') == species_schema.dump(species).data

            fin.pop('species')
            fin.pop('owner')
            assert fin == ori

            # deleting table before removing dummy species
            animal_stored.delete(session=s)


@given(name = st.text(),
    happy = st.integers(min_value=-2147483648, max_value=2147483647),
    hungry = st.integers(min_value=-2147483648, max_value=2147483647)
)
def test_load_animals_NO_species_id_FAIL(name, happy, hungry):

    with clean_memorydb_session_from_schema(animal_schema) as s:
        ori = {'name': name, 'happy': happy, 'hungry': hungry}

        # load our dict
        animal_data, animal_errors = animal_schema.load(ori, session=s)

        # assert we can NOT save it
        with pytest.raises(Exception):
            animal_data.save(session=s)


@given(name = st.text(),
    happy = st.integers(min_value=-2147483648, max_value=2147483647),
    hungry = st.integers(min_value=-2147483648, max_value=2147483647)
)
def test_load_animals_species_FAIL(name, happy, hungry):

    with clean_memorydb_session_from_schema(animal_schema) as s:

        with dummy_species(s) as species:

            ori = {'name': name, 'happy': happy, 'hungry': hungry, 'species': species}

            # load our dict
            animal_data, animal_errors = animal_schema.load(ori, session=s)

            # assert we can NOT save it
            with pytest.raises(Exception):
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