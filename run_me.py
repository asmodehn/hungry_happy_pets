import os

import click

from app import create_app

from flask_migrate import Migrate

# default config to dev for now
# TODO : change this after first version working
config_name = os.getenv('APP_SETTINGS') or "development"

# instantiate the app
app, db = create_app(config_name)

# instantiate migration context
migrate = Migrate(app, db)


@app.cli.command()
def testcmd():
    """Test the command."""
    click.echo('Test the cmd')


# for default action
if __name__ == '__main__':
    app.run()
