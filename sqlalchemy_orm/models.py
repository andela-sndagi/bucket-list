# sqlalchemy_orm/models.py
import os, sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy_orm.app import app

db = SQLAlchemy(app)


class Bucketlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    date_created = db.Column(db.DateTime,
                             default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    created_by = db.Column(db.String(20), unique=True)


class BucketlistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    bucketlist = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))
    bucketlist_id = db.relationship('Bucketlist', backref='items')
    date_created = db.Column(db.DateTime,
                             default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    done = db.Column(db.Boolean, default=False)
