from peewee import * # ORM
import datetime, os
from passlib.hash import sha256_crypt

db = SqliteDatabase('bucketlist.db')

class User(Model):
    """
    Model for User Table
    """
    id = PrimaryKeyField()
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    def set_password(self):
        return sha256_crypt.encrypt(self.password)

    # Override save method for this model
    # The password is now saved as hashed in the DB
    def save(self):
        self.password = self.set_password()
        super(User, self).save()

    # Boolean statement
    def valid_password(self, entered_password):
        password = self.set_password()
        return sha256_crypt.verify(entered_password, self.password)

    # Is dependent on the valid_login function
    def log_the_user_in(self):
        return str(os.urandom(12).encode('hex'))

    class Meta:
        database = db


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
    id = PrimaryKeyField()
    bl_id = ForeignKeyField(Bucketlist, related_name='items')
    name = CharField()
    date_created = DateTimeField(default = datetime.datetime.now)
    date_modified = DateTimeField(default = datetime.datetime.now)
    done = BooleanField()

    class Meta:
        database = db


def initialize_db():
    db.connect()
    db.create_tables([User, Bucketlist, BucketlistItem], safe=True)
