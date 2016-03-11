class Config(object):
    """Default Settings"""
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """setting Testing configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bucketlist.db'

class TestingConfig(Config):
    """setting Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

CONFIG = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}
