# sqlalchemy_orm/app.py

import os, sys
import inspect
# currentdir = os.path.dirname(os.path.abspath(
#     inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0, parentdir)

from flask import request
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api, fields, marshal_with, Resource
from sqlalchemy import create_engine, desc, func, orm


# Resources
from resources import Index
from resources.users import Register, Login
from resources.bucketlists import Bucketlists
from resources.bucketlist_items import BucketlistItems
from resources.single_bucketlist import SingleBucketlist
from resources.single_bucketlist_item import SingleBucketlistItem


access_denied = {"message": "Not authorized"}

# Initialise Flask
app = Flask(__name__)

# Database instance
db = SQLAlchemy(app)

auth = HTTPBasicAuth()

app.config.from_object('sqlalchemy_orm.config.DevelopmentConfig')

# def init_session():
#     """
#     Configures the current database and returns a session instance for use
#     during CRUD operations.
#     """
#     engine = create_engine(app.config.get('SQLALCHEMY_DATABASE_URI'))
#     session = orm.sessionmaker()
#     session.configure(bind=engine)
#     return session()

# init = init_session()



def get_request_token():
    """
    Retrieve a user's token from the username key of the request's header.
    """
    return request.headers.get('username')


def is_bucketlist_owner(bucketlist):
    token = get_request_token()
    # Ensure the owner of the bucketlist is the only one who can update it
    if User.verify_auth_token(token).username == bucketlist.created_by:
        return True
    return False

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

# Instance of Api
api = Api(app)

# URLs
api.add_resource(Index, '/')
api.add_resource(Register, '/auth/register/')
api.add_resource(Login, '/auth/login/')
api.add_resource(Bucketlists, '/bucketlists/')
api.add_resource(SingleBucketlist, '/bucketlists/<int:id>')
api.add_resource(BucketlistItems, '/bucketlists/<int:id>/items/')
api.add_resource(SingleBucketlistItem, '/bucketlists/<int:id>/items/<int:item_id>')
