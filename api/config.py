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
