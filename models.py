from peewee import *
import datetime

db = SqliteDatabase('bucketlists.db')

class Bucketlist(Model):
    id = PrimaryKeyField()
    name = CharField()
    date_created = DateTimeField(default = datetime.datetime.now)
    date_modified = DateTimeField(default = datetime.datetime.now)
    created_by = CharField()


    class Meta:
        database = db

def initialize_db():
    db.connect()
    db.create_tables([Bucketlist], safe=True)

