# sqlalchemy_orm/app.py

import os, sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask.ext.script import Manager, prompt_bool
from flask_restful import Api, fields, marshal_with, Resource
from sqlalchemy_orm.models import Bucketlist, BucketlistItem, app, initialise, drop

# Resources
from resources import Index
from resources.bucketlists import Bucketlists
from resources.bucketlist_items import BucketlistItems
from resources.single_bucketlist import SingleBucketlist
from resources.single_bucketlist_item import SingleBucketlistItem


# Setup manager to allow runserver, shell and migrate at runtime
manager = Manager(app)

@manager.command
def start():
    """Start Application by creating Database and tables within."""
    print "Bucketlist API is initialising... \n(If it is your first RUN you will have demo data according to the TASK segment in the README)\n  (If you want to do away with previous data and start)\n     RUN 'python api.py exit' afterwhich you\n     RUN 'python api.py start' \n  Otherwise proceed to run the app 'python api.py runserver'"
    initialise()

@manager.command
def exit():
    """Exit application by deleting Database and its contents."""
    if prompt_bool(
    "Bucketlist API is exitting...\n\
    Are you sure you want to exit and lose all your data?\n\
        Type 'Y/y' - YES\n\
        Type 'N/n' - NO"):
        drop()

# Instance of Api
api = Api(app)

# URLs
api.add_resource(Index, '/')
api.add_resource(Bucketlists, '/bucketlists/')
api.add_resource(SingleBucketlist, '/bucketlists/<int:id>')
api.add_resource(BucketlistItems, '/bucketlists/<int:id>/items/')
api.add_resource(SingleBucketlistItem, '/bucketlists/<int:id>/items/<int:item_id>')
