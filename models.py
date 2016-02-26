from peewee import *  # ORM
import datetime, os

# Database object you wish to use
db = SqliteDatabase('bucketlist.db')

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


def initialize_db():
    db.connect()
    db.create_tables([Bucketlist, BucketlistItem], True)
