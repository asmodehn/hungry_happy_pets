
import contextlib
from app import create_app, models

from app import schemas


@contextlib.contextmanager
def clean_app_test_client(config_name):
    app = create_app(config_name=config_name)
    client = app.test_client

    # binds the app to the current context
    with app.app_context():
        # create all tables
        models.db.create_all()

        yield client()

        # drop all tables just in case
        models.db.session.remove()
        models.db.drop_all()


# Dummy schemas save, rely ony on the underlying schemas (which should already work)
# so we dont test anything here
@contextlib.contextmanager
def dummy_user(nick=None, email=None):

    # generating a user from hypothesis data via marshmallow
    user_loaded = schemas.user_schema.load({'nick': nick or 'testuser', 'email': email or 'tester@comp.any'})
    user = user_loaded.data

    # writing to DB
    user.save()

    yield schemas.user_schema.dump(user).data

    user.delete()

@contextlib.contextmanager
def dummy_user_list(nick_email_list=None):

    nick_email_list = nick_email_list or [('testuser', 'tester@comp.any')]

    user_list = []

    for nick, email in nick_email_list:
        # generating a user from hypothesis data via marshmallow
        user_loaded = schemas.user_schema.load({'nick': nick, 'email': email})
        user = user_loaded.data

        # writing to DB
        user.save()
        user_list.append(user)

    yield [schemas.user_schema.dump(u).data for u in user_list]

    for u in user_list:
        u.delete()


@contextlib.contextmanager
def dummy_owner(nick=None, email=None):

    with dummy_user(nick=nick, email=email) as user_data:

        # generating a owner from hypothesis data via marshmallow
        owner_loaded = schemas.owner_schema.load({'user_id': user_data.get('id')})
        owner = owner_loaded.data

        # writing to DB
        owner.save()

        yield schemas.user_schema.dump(owner).data

        owner.delete()


@contextlib.contextmanager
def dummy_owner_list(nick_email_list=None):

    nick_email_list = nick_email_list or [('testuser', 'tester@comp.any')]

    with dummy_user_list(nick_email_list=nick_email_list) as user_data_list:
        owner_list = []

        for user_data in user_data_list:
            # generating a owner from hypothesis data via marshmallow
            owner_loaded = schemas.owner_schema.load({'user_id': user_data.id})
            owner = owner_loaded.data

            # writing to DB
            owner.save()

            owner_list.append(owner)

        yield [schemas.owner_schema.dump(o).data for o in owner_list]

        for o in owner_list:
            o.delete()


@contextlib.contextmanager
def dummy_species(name=None, happy_rate=None, hunger_rate=None):

    # generating a species from hypothesis data via marshmallow
    species_loaded = schemas.species_schema.load({'name': name or 'testspecies', 'happy_rate': happy_rate or 5, 'hunger_rate': hunger_rate or 23})
    species = species_loaded.data

    # writing to DB
    species.save()

    yield schemas.species_schema.dump(species).data

    species.delete()

#
# @contextlib.contextmanager
# def dummy_animal(session):
#     with dummy_species(session) as species_data:
#         animal_data = models.Animal(name='testanimal', happy=4, hungry=42)
#         animal_data.species_id = species_data.id
#         animal_data.save(session=session)
#
#         yield animal_data
#
#         animal_data.delete(session=session)
