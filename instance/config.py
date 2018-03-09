import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:////tmp/hungry_happy_pets.db'  # sqlite by default

class TestingConfig(Config):
    """Configurations for Testing, with a separate in memory test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # quick testing
    DEBUG = True

class StagingConfig(Config):
    """Configurations for Heroku deployed app."""
    DEBUG = True
    TESTING = False

class HerokuConfig(Config):
    """Configurations for Heroku deployed app."""
    DEBUG = True
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'heroku': HerokuConfig,
}
