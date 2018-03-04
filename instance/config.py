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
    """Configurations for Staging."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'postgresql://localhost/test_db'  # same as prod
    DEBUG = True

class ProductionConfig(StagingConfig):
    """Configurations for Production as close as possible from staging."""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    # preventing accidents ith untested configs.
    # 'staging': StagingConfig,
    # 'production': ProductionConfig,
}
