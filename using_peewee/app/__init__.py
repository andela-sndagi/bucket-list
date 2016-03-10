# !/usr/bin/python
# title          :Main app file
# description    :REST API allowing CRUD of bucketlists and bucketlists items
# author         :Stanley Ndagi
# email          :stanley.ndagi@andela.com
# date           :20160310
# version        :0.0.2
# python_version :2.7.10
# ==============================================================================

import os, sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask import Flask
from flask.ext.script import Manager
from flask_restful import Api
from flask_environments import Environments

# Configuration
from config import CONFIG

# Resources
from resources import Index
from resources.bucketlists import Bucketlists
from resources.bucketlist import Bucketlist
from resources.bucketlist_items import BucketlistItems
from resources.bucketlist_item import BucketlistItem

# Models
from models import initialize_db, db


# Initialise Flask
app = Flask(__name__)

# Setup the environment for the app from config file
env = Environments(app)
env.from_object(CONFIG['development'])

# Setup manager to allow runserver, shell and migrate at runtime
manager = Manager(app)

# Add command to initialize the app by creating db and tables
@manager.command
def start():
    """Initialize the app by creating db and tables"""
    initialize_db()


@app.before_request
def before_request():
    # create db if needed and connect
    db.connect()


@app.teardown_request
def teardown_request(exception):
    # close the db connection
    db.close()


api = Api(app)

api.add_resource(Index, '/')
api.add_resource(Bucketlists, '/bucketlists/')
api.add_resource(Bucketlist, '/bucketlists/<int:list_id>')
api.add_resource(BucketlistItems, '/bucketlists/<int:list_id>/items/')
api.add_resource(BucketlistItem, '/bucketlists/<int:list_id>/items/<int:item_id>')
