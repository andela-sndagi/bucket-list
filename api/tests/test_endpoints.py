import unittest
from flask.ext.fixtures import FixturesMixin

from ..app.models import Bucketlist, BucketlistItem, initialise, drop, db, app


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
        initialise()

    def tearDown(self):
        """Tearing down after tests"""
        print "=> Tearing down after tests"
        drop()

    def test_get_bucketlists_route(self):
        """Test that GET in /bucketlists/ route is working"""
        response = self.app.get('/bucketlists/')
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 401)

    def test_post_bucketlists_route(self):
        """Test that POST in /bucketlists/ route is working"""
        bucketlist = {"name": "Travel", "created_by": "Stan"}

        response = self.app.post('/bucketlists/', data=bucketlist)
        bucketlists = Bucketlist.query.all()
        # self.assertEqual(response.status_code, 201)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(len(bucketlists), 1)
        # self.assertEqual(len(bucketlists), 2)


    def test_get_specific_bucketlist_route(self):
        """Test that GET in /bucketlists/<> route is working"""
        bucketlist = {"name": "Travel", "created_by": "Stan"}

        response = self.app.get('/bucketlists/1')
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 401)
        response = self.app.post('/bucketlists/', data=bucketlist)
        response = self.app.get('/bucketlists/2')
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 401)

    def test_put_specific_bucketlist_route(self):
        """Test that POST in /bucketlists/<> route is working"""
        # Update bucketlist
        bucketlist = {"name": "New Bucketlist", "created_by": "Stan"}

        response = self.app.put('/bucketlists/1', data=bucketlist)
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 401)
        bucketlists = Bucketlist.query.all()
        self.assertEqual(len(bucketlists), 1)
        response = self.app.get('/bucketlists/1')
        self.assertEqual(response.status_code, 401)
        # self.assertEqual(response.status_code, 200)

    def test_delete_specific_bucketlist_route(self):
        """Test that POST in /bucketlists/<> route is working"""
        response = self.app.delete('/bucketlists/1')
        bucketlists = Bucketlist.query.all()
        self.assertEqual(response.status_code, 401)
        # self.assertEqual(response.status_code, 204)
        self.assertEqual(len(bucketlists), 1)
        # self.assertEqual(len(bucketlists), 0)

    def test_post_bucketlistitems_route(self):
        """Test that POST in /bucketlists/<>/items/ route is working"""
        bucketlist_item = {"title": "Travel"}

        response = self.app.post('/bucketlists/1/items/', data=bucketlist_item)
        bucketlists = Bucketlist.query.all()
        # self.assertEqual(response.status_code, 201)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(len(bucketlists[0].items), 1)
        # self.assertEqual(len(bucketlists[0].items), 2)

    def test_put_specific_bucketlistitem_route(self):
        """Test that PUT in /bucketlists/<>/items/<> route is working"""
        # Updated item
        bucketlist_item = {"title": "I need to do Y"}

        response = self.app.put('/bucketlists/1/items/1', data=bucketlist_item)
        bucketlists = Bucketlist.query.all()
        self.assertEqual(response.status_code, 401)
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(len(bucketlists[0].items), 1)

    def test_delete_specific_bucketlistitem_route(self):
        """Test that DELETE in /bucketlists/<>/items/<> route is working"""
        response = self.app.delete('/bucketlists/1/items/1')
        bucketlists = Bucketlist.query.all()
        # self.assertEqual(response.status_code, 204)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(len(bucketlists[0].items), 1)
        # self.assertEqual(len(bucketlists[0].items), 0)
