import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET') or b'\xf1b\x1b\xad\x85\x9fw)}n\x060.\xd4cn3\xc9\x10\x82\xdbl\xae\xc2'  # random dev secret key
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:////tmp/hungry_happy_pets.db'  # sqlite by default


class TestingConfig(DevelopmentConfig):
    """Configurations for Testing, with a separate in memory test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # quick testing


class StagingConfig(Config):
    """Configurations for Heroku local|staging app."""
    DEBUG = True
    TESTING = False


class HerokuConfig(StagingConfig):
    """Configurations for Heroku deployed app."""
    DEBUG = True


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'heroku': HerokuConfig,
}
