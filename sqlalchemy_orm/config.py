# sqlalchemy_orm/config.py

import os, sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


class TestConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    testing = True
    debug = True
