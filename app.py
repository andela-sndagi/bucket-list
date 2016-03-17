# bucketlist/app.py

import os, sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful import Api

# Resources
from resources import Index

# Initialise Flask
app = Flask(__name__)

# Database instance
db = SQLAlchemy(app)


# Instance of Api
api = Api(app)

# URLs
api.add_resource(Index, '/')

