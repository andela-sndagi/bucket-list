# sqlalchemy_orm/app

import os, sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


from flask import Flask
# from flask.ext.script import Manager
# from flask_restful import Api



# Resources
# from resources import Index
# from resources.bucketlists import Bucketlists
# from resources.bucketlist_items import BucketlistItems


# Initialise Flask
app = Flask(__name__)
# app.config.update(
#     DATABASE_URI='sqlite://')

# Setup manager to allow runserver, shell and migrate at runtime
# manager = Manager(app)

# # Instance of Api
# api = Api(app)

# # URLs
# api.add_resource(Index, '/')
# api.add_resource(Bucketlists, '/bucketlists/')
# api.add_resource(BucketlistItems, '/bucketlists/<int:list_id>/items/')
