# !/usr/bin/python
# title          :run.py
# description    :Allocates persons to rooms in a building
# author         :Stanley Ndagi
# email          :stanley.ndagi@andela.com
# date           :20160304
# version        :0.0.1
# python_version :2.7.10
# ==============================================================================

# Importation error fixing
import os, sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask import Flask, Blueprint
from flask.ext.script import Manager
from flask_restful import Api
from flask_environments import Environments

from resources import Index
from resources.bucketlists import Bucketlists
from resources.bucketlist import Bucketlist
from resources.bucketlist_items import BucketlistItems
from resources.bucketlist_item import BucketlistItem

# from config import config
from config import config

app = Flask(__name__)  # Initialise Flask

# Setup the environment for the app from config file
env = Environments(app)
env.from_object(config['development'])

# Setup manager to allow runserver and shell at runtime
manager = Manager(app)


api_bp = Blueprint('api', __name__)
api = Api(api_bp)
manager = Manager(app)

api.add_resource(Index, '/')
# api.add_resource(Bucketlists, '/bucketlists/')
# api.add_resource(Bucketlist, '/bucketlists/<int:id>')
# api.add_resource(BucketlistItems, '/bucketlists/<int:id>/items/')
# api.add_resource(BucketlistItem, '/bucketlists/<int:id>/items/<int:itemid>')


app.register_blueprint(api_bp)


if __name__ == '__main__':
    manager.run()
