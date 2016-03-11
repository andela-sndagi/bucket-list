# ORM (One can use Peewee instead)
from flask.ext.sqlalchemy import SQLAlchemy

import app


db = SQLAlchemy(app)


class Bucketlist(db.Model):
    """
    Model for Bucketlist Table extending BaseModel
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.String(30))


class BucketlistItem(db.Model):
    """
    Model for BucketlistItem Table
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))
    bucketlist = db.relationship('Bucketlist', backref='items')
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    done = db.Column(db.BooleanField, default=False)
