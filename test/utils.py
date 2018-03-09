
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
def dummy_owner(session):

    with dummy_user(session) as user_data:

        # generating a owner from hypothesis data via marshmallow
        owner_loaded = schemas.owner_schema.load({'user_id': user_data.id})
        owner = owner_loaded.data

        # writing to DB
        owner.save()

        yield schemas.user_schema.dump(owner).data

        owner.delete()

#
# @contextlib.contextmanager
# def dummy_species(session):
#     species_data = models.Species(name='testspecies', happy_rate=5, hunger_rate=23)
#     species_data.save(session=session)
#
#     yield species_data
#
#     species_data.delete(session=session)
#
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
