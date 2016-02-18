import os
import base64
from peewee import * # ORM


from app import initialize_db, db

initialize_db()

import app
test_app = app.app.test_client()

def teardown():
  db_session.remove()