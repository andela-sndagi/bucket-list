# sqlalchemy_orm/config.py

import os, sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


class Config(object):
    """Default Settings"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = "some_random_key"


class DevelopmentConfig(Config):
    """setting Testing configuration"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bucketlists.db'
    DEBUG = True


class TestConfig(Config):
    """setting Testing configuration"""
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True
