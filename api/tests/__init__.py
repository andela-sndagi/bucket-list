import unittest

from flask.ext.fixtures import FixturesMixin
from ..app.models import User, Bucketlist, BucketlistItem
from ..app.models import initialise, drop, db, app


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
        # Add configuration to the app
        app.config.update({'TESTING': True})
        self.app = app.test_client()
        initialise()

    def tearDown(self):
        """Tearing down after tests"""
        print "=> Tearing down after tests"
        drop()

    def test_api_index(self):
        """Test if the index page is working"""
        response = self.app.get('/')
        print '=> Getting to "/"'
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bucket List Service API is ready', response.data)

    def test_users_items_in_fixtures(self):
        """Test user entries in fixtures"""
        users = User.query.all()
        self.assertEqual(len(users) == User.query.count(), 1)

    def test_bucketlists_in_fixtures(self):
        """Test bucket-list entries in fixtures"""
        bucketlists = Bucketlist.query.all()
        self.assertEqual(len(bucketlists) == Bucketlist.query.count(), 1)
        u1 = User.query.filter(User.username == 'User1').first()
        for bucketlist in bucketlists:
            assert bucketlist.created_by == u1.id

    def test_bucketlist_items_in_fixtures(self):
        """Test bucket-list items entries in fixtures"""
        items = BucketlistItem.query.all()
        self.assertEqual(len(items) == Bucketlist.query.count(), 1)
        bl1 = Bucketlist.query.filter(Bucketlist.name == 'BucketList1').first()
        for item in items:
            assert item.bucketlist == 1
