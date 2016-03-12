# sqlalchemy_orm/tests.py

import os, sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import unittest

from flask.ext.fixtures import FixturesMixin

from sqlalchemy_orm.app import app
from sqlalchemy_orm.models import db, Bucketlist, BucketlistItem


# Configure the app with the testing configuration
app.config.from_object('sqlalchemy_orm.config.TestConfig')

# Initialize the Flask-Fixtures mixin class
FixturesMixin.init_app(app, db)


class AppTestCase(unittest.TestCase, FixturesMixin):
    """
    AppTestCase
    Make sure to inherit from the FixturesMixin class
    """

    # Specify the fixtures file(s) you want to load
    fixtures = ['bucketlists.json']

    def setUp(self):
        """Setting up the environment for testing"""
        print "=> Setting up the environment for testing"
        self.app = app.test_client()

    def tearDown(self):
        """Tearing down after tests"""
        print "=> Tearing down after tests"

    def test_api_index(self):
        """Test if the index page is working"""
        response = self.app.get('/')
        print '=> Getting to "/"'
        assert response.status == "200 OK"
        self.assertIn('Bucket List Service API is ready', response.data)

    def test_bucketlists(self):
        """Test bucketlist entries in fixtures"""
        bucketlists = Bucketlist.query.all()
        self.assertEqual(len(bucketlists) == Bucketlist.query.count(), 1)
        self.assertEqual(len(bucketlists[0].items), 1)

    def test_bucketlist_items(self):
        """Test bucketlistitems entries in fixtures"""
        items = BucketlistItem.query.all()
        self.assertEqual(len(items) == Bucketlist.query.count(), 1)
        bl1 = Bucketlist.query.filter(Bucketlist.name == 'BucketList1').one()
        for item in items:
            assert item.bucketlist_id == bl1

    def test_get_bucketlists_route(self):
        """Test that /bucketlists/ route is working"""
        self.app = app.test_client()
        response = self.app.get('/bucketlists/')
        self.assertEqual(response.status, '200 OK')

    def test_bucketlist_items_route(self):
        """Test that /bucketlists/ route is working"""
        self.app = app.test_client()
        response = self.app.get('/bucketlists/1/items/')
        self.assertEqual(response.status, '200 OK')
