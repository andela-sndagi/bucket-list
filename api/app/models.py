from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask.ext.httpauth import HTTPBasicAuth

# declare auth to be used for authentication
auth = HTTPBasicAuth()

# Initialize Flask
app = Flask(__name__)

# Initialize the database
db = SQLAlchemy(app)


class User(db.Model):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(128))

    def hash_password(self, password):
        """Hash the password to be saved in db"""
        return pwd_context.encrypt(password)

    def verify_password(self, password):
        """Verifies the password entered against the hashed one in the db
           Returns true if the password entered is correct"""
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=3600):
        """Generates the token for authentication and inserts the user id in it to
           uniquely identify the user by decoding the token itself"""
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        """Verify the token entered in the header then returns the user
           associated with the token"""
        s = Serializer(app.config['SECRET_KEY'])
        if token is None:
            return {}
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

    #  Constructor for User
    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)

    def __repr__(self):
        return self.username


class Bucketlist(db.Model):
    """Model for Bucketlist"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    date_created = db.Column(db.DateTime,
                             default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    #  Constructor for Bucket-list
    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by

    def __repr__(self):
        return '<Bucketlist {}>'.format(self.name)


class BucketlistItem(db.Model):
    """Model for item in Bucketlist"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    bucketlist = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))
    date_created = db.Column(db.DateTime,
                             default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp())
    done = db.Column(db.Boolean, default=False)

    #  Constructor for BucketlistItem
    def __init__(self, title, bucketlist):
        self.title = title
        self.bucketlist = bucketlist

    def __repr__(self):
        return '<Item {}>'.format(self.title)


def initialise():
    """Initialize app by creating db and its dependencies"""
    db.create_all()

def drop():
    """Delete db and its contents"""
    db.drop_all()
