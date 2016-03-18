# bucketlist/config.py


class Config(object):
    """Default Settings"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = "thequickbrownfoxjumpedoverthelazydog"


class DevelopmentConfig(Config):
    """setting Development configuration"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bucketlists.db'
    DEBUG = True


class TestConfig(Config):
    """setting Testing configuration"""
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True
