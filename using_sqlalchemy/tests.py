import os, sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import unittest
from flask_environments import Environments
# from peewee import SqliteDatabase
# from playhouse.test_utils import test_database
from app import app
from app.models import db, Bucketlist, BucketlistItem
import config

db = SqliteDatabase(':memory:')

from flask.ext.fixtures import FixturesMixin

# Configure the app with the testing configuration
# env = Environments(app)
# env.from_object(config.CONFIG['testing'])
# app.config.from_object('app.config.TestingConfig')

# Initialize the Flask-Fixtures mixin class
FixturesMixin.init_app(app, db)


# Make sure to inherit from the FixturesMixin class
class AppTestCase(unittest.TestCase, FixturesMixin):
    """App TestCase"""
    fixtures = ['bucketlists.json']

    # def setUp(self):
    #     """Setting up the environment for testing"""
    #     print "=> Setting up the environment for testing"
    #     for i in range(5):
    #         models.Bucketlist.create(name='bucketlist-%d' % i, created_by='3123%d' % i)
    #         # for j in range(10):
    #         #     models.BucketlistItem.create(name='bucketlistitem-%d' % j, bucketlist= % i)

    # def tearDown(self):
    #     """Tearing down after tests"""
    #     print "=> Tearing down after tests"
    #     models.db.close()

    def test_fixtures(self):
        bucketlists = Bucketlist.select()
        import ipdb; ipdb.set_trace()
        self.assertEqual(len(bucketlists), 1)
        self.assertEqual(len(bucketlists[0].items), 1)

    # def test_api_index(self):
    #     """Test if the index page is working"""
    #     response = self.app.get('/')
    #     print '=> Getting to "/"'
    #     assert response.status == "200 OK"
    #     self.assertIn('Bucket List Service API is ready', response.data)

    # def test_get_bucketlists(self):
    #     """Test if the /bucketlists/ endpoint"""
    #     response = self.app.get('/bucketlists/')
    #     print '=> Getting to "/bucketlists/"'
    #     assert response.status == "200 OK"
    #     # self.assertEqual([], response.data)

if __name__ == '__main__':
    unittest.main()
