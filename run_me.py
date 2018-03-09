import os

import click

from app import create_app, models
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

# default config to dev for now
# TODO : change this after first version working
config_name = os.getenv('APP_SETTINGS') or "development"

# instantiate the app ( access via "flask shell" or "flask run" command )
app = create_app(config_name)

admin = Admin(app, name='happy-hungry-pets', template_mode='bootstrap3')

# Add administrative views here
admin.add_view(ModelView(models.User, models.db.session))
admin.add_view(ModelView(models.Owner, models.db.session))
admin.add_view(ModelView(models.Species, models.db.session))
admin.add_view(ModelView(models.Animal, models.db.session))


# instantiate migration context ( access via "flask db" command )
migrate = Migrate(app, models.db)


@app.cli.command()
def testcmd():
    """Test the command."""
    click.echo('Test the cmd')


# for default action
if __name__ == '__main__':
    app.run()
