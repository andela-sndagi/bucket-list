# ORM (One can use SQLAlchemy instead)
from peewee import SqliteDatabase, PrimaryKeyField, CharField
from peewee import DateTimeField, datetime, ForeignKeyField, Model, BooleanField


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
    id = PrimaryKeyField(unique=True)
    name = CharField(unique=True)
    date_created = DateTimeField(default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    date_modified = DateTimeField(default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    created_by = CharField()


class BucketlistItem(BaseModel):
    """
    Model for BucketlistItem Table
    """
    id = PrimaryKeyField()
    bucketlist = ForeignKeyField(Bucketlist, related_name='items')
    name = CharField(unique=True)
    date_created = DateTimeField(default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    date_modified = DateTimeField(default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    done = BooleanField(default=False)


def initialize_db():
    """Create tables based on the models in the specified db"""
    db.create_tables([Bucketlist, BucketlistItem], True)
