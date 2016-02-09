from peewee import * # ORM
import datetime

db = SqliteDatabase('bucketlist.db')

class Bucketlist(Model):
    """
    Model for Bucketlist Table
    """

    id = PrimaryKeyField()
    name = CharField()
    date_created = DateTimeField(default = datetime.datetime.now)
    date_modified = DateTimeField(default = datetime.datetime.now)
    created_by = CharField()

    class Meta:
        database = db


class BucketlistItem(Model):
    """
    Model for BucketlistItem Table
    """
    id = ForeignKeyField(Bucketlist, related_name='items')
    item_id = PrimaryKeyField()
    name = CharField()
    date_created = DateTimeField(default = datetime.datetime.now)
    date_modified = DateTimeField(default = datetime.datetime.now)
    done = BooleanField()

    class Meta:
        database = db


def initialize_db():
    db.connect()
    db.create_tables([Bucketlist, BucketlistItem], safe=True)
