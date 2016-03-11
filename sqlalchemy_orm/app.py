# !/usr/bin/python
# title          :Main app file
# description    :REST API allowing CRUD of bucketlists and bucketlists items
# author         :Stanley Ndagi
# email          :stanley.ndagi@andela.com
# date           :20160310
# version        :0.0.2
# python_version :2.7.10
# ==============================================================================

from flask import Flask
from flask.ext.script import Manager
from flask_restful import Api

# Resources
from resources import Index

# Initialise Flask
app = Flask(__name__)

# Setup manager to allow runserver, shell and migrate at runtime
manager = Manager(app)

# Instance of Api
api = Api(app)

# Urls
api.add_resource(Index, '/')
