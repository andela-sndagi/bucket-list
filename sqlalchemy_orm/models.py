# sqlalchemy_orm/models.py

import os, sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

from passlib.apps import custom_app_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as tokenizer, BadSignature, SignatureExpired)


# Initialise Flask
app = Flask(__name__)

# Database instance
db = SQLAlchemy(app)

auth = HTTPBasicAuth()

class User(db.Model):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(128))

    def hash_password(self, password):
        return custom_app_context.encrypt(password)

    #  Constructor for User
    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)

    def __repr__(self):
        return '<User %r>' % self.username

    def verify_password(self, password):
        return custom_app_context.verify(password, self.password)


    def generate_token(self, expiration=300):
        s = tokenizer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = tokenizer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user


class Bucketlist(db.Model):
    """Model for Bucketlist"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_id = db.relationship('User', backref='bucketlist')
    date_created = db.Column(db.DateTime,
                             default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp())
    created_by = db.Column(db.String(20))

    #  Constructor for Bucketlist
    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by

    def __repr__(self):
        return '<Bucketlist %r>' % self.name


class BucketlistItem(db.Model):
    """Model for item in Bucketlist"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    bucketlist = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))
    bucketlist_id = db.relationship('Bucketlist', backref='items')
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
        return '<Item %r>' % self.title


def initialise():
    """Initialize app by creating db and its dpendencies"""
    db.create_all()

def drop():
    """Delete db and its conten"""
    db.drop_all()
