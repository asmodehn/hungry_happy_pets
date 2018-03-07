
import contextlib
from app import create_app, models

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
