# ORM
from peewee import SqliteDatabase, PrimaryKeyField, CharField, DateTimeField, ForeignKeyField, Model, BooleanField
from flask import g
import datetime, os

db = SqliteDatabase('bucketlist_app.db')


def initialize_db():
    # g.db = SqliteDatabase(database)
    # # using g object to 'globalize' the db
    db.connect()



class BaseModel(Model):
    """
    Parent model including pointing at the database
    """
    class Meta:
        database = db


class Bucketlist(BaseModel):
    """
    Model for Bucketlist Table extending BaseModel
    """
    id = PrimaryKeyField()
    name = CharField(unique=True)
    date_created = DateTimeField(default = datetime.datetime.now)
    date_modified = DateTimeField(default = datetime.datetime.now)
    created_by = CharField()


class BucketlistItem(BaseModel):
    """
    Model for BucketlistItem Table
    """
    id = PrimaryKeyField()
    bucketlist = ForeignKeyField(Bucketlist, related_name='items')
    name = CharField()
    date_created = DateTimeField(default = datetime.datetime.now)
    date_modified = DateTimeField(default = datetime.datetime.now)
    done = BooleanField()


# To be executed after
def create_tables():
    db.create_tables([Bucketlist, BucketlistItem], True)