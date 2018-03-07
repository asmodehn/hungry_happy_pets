
import contextlib

import sqlalchemy
from app.schemas import models


@contextlib.contextmanager
def clean_memorydb_session_from_schema(schema):
    engine = sqlalchemy.create_engine('sqlite:///:memory:')
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()

    schema.Meta.model.metadata.create_all(engine)

    yield session

    schema.Meta.model.metadata.drop_all(engine)
    session.close()


# Dummy table rows, rely ony on the core model DB (which should already work)
# so we dont test anything here
def dummy_user(session):

    user_data = models.User(nick='testuser', email='tester@comp.any')
    user_data.save(session=session)

    yield user_data

    user_data.delete(session=session)


def dummy_owner(session):

    with dummy_user(session) as user_data:
        owner_data = models.Owner()
        owner_data.user_id = user_data.id

        yield owner_data, user_data

        owner_data.delete(session=session)


def dummy_species(session):
    species_data = models.Species(name='testspecies', happy_rate=5, hunger_rate=23)
    species_data.save(session=session)

    yield species_data

    species_data.delete(session=session)


def dummy_animal(session):
    with dummy_species(session) as species_data:
        animal_data = models.Animal(name='testanimal', happy=4, hungry=42)
        animal_data.species_id = animal_data.id

        yield animal_data, species_data

        animal_data.delete(session=session)

