# sqlalchemy_orm/models.py

import os, sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Initialise Flask
app = Flask(__name__)

# Database instance
db = SQLAlchemy(app)


class Bucketlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
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
    db.create_all()

def drop():
    db.drop_all()
