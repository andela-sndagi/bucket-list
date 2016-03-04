from flask import Flask, g
from flask.ext.script import Manager
from peewee import SqliteDatabase
from flask_environments import Environments

import config


from models import Bucketlist, BucketlistItem, initialize_db, create_tables

app = Flask(__name__)  # Initialise Flask

# Setup the environment for the app from config file
env = Environments(app)
env.from_object(config.DevelopmentConfig)

# Setup manager to allow runserver and shell at runtime
manager = Manager(app)




@app.before_request
def before_request():
    """create db if needed and connect"""
    initialize_db()
    create_tables()



@app.teardown_request
def teardown_request(exception):
    """Close the db connection"""
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


# Route handler
@app.route('/', methods=(['GET']))
def api_index():
    """View function: Welcome note at index"""
    return "Bucket List Service API is ready"
