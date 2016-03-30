import json
import unittest
from flask.ext.fixtures import FixturesMixin

from ..app.models import Bucketlist, BucketlistItem, User
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
        app.config.update({'TESTING': True, 'SECRET_KEY': "abcdefgh"})
        self.app = app.test_client()
        initialise()

    def tearDown(self):
        """Tearing down after tests"""
        print "=> Tearing down after tests"
        drop()

    def get_token(self):
        """Login to return token for authentication"""
        data = json.dumps({'username': 'User1', 'password': 'p@ssw0rd'})
        response = self.app.post('/auth/login/', data=data, content_type='application/json')
        token = json.loads(response.data).get('token')
        return token

    def test_get_bucketlists_route(self):
        """Test that GET in /bucketlists/ route is working"""

        # Test route without token
        response = self.app.get('/bucketlists/')
        self.assertEqual(response.status_code, 401)

        # Test route with token
        response = self.app.get('/bucketlists/', headers={'token': self.get_token()})
        self.assertEqual(response.status_code, 200)
        bucketlists = json.loads(response.data).get('bucketlists')
        self.assertEqual(len(bucketlists), 1)


    def test_post_bucketlists_route(self):
        """Test that POST in /bucketlists/ route is working"""
        bucketlist = json.dumps({"name": "Travel"})

        # Test route without token
        response = self.app.post('/bucketlists/', data=bucketlist)
        bucketlists = Bucketlist.query.all()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(len(bucketlists), 1)

        # Test route with token
        response = self.app.post('/bucketlists/',
                                 data=bucketlist,
                                 headers={'token': self.get_token(),
                                          'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 201)

    def test_get_specific_bucketlist_route(self):
        """Test that GET in /bucketlists/<> route is working"""

        # Test route without token
        response = self.app.get('/bucketlists/1')
        self.assertEqual(response.status_code, 401)

        # Test route with token
        response = self.app.get('/bucketlists/1',
                                headers={'token': self.get_token()})
        self.assertEqual(response.status_code, 200)

    def test_put_specific_bucketlist_route(self):
        """Test that POST in /bucketlists/<> route is working"""
        # Update bucketlist
        bucketlist = json.dumps({"name": "New Bucketlist"})

        # Test route without token
        response = self.app.put('/bucketlists/1', data=bucketlist)
        self.assertEqual(response.status_code, 401)

        # Test route with token
        response = self.app.put('/bucketlists/1',
                                 data=bucketlist,
                                 headers={'token': self.get_token(),
                                          'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['message'], "Bucketlist #1 Successfully updated")

    def test_delete_specific_bucketlist_route(self):
        """Test that POST in /bucketlists/<> route is working"""

        # Test route without token
        response = self.app.delete('/bucketlists/1')
        self.assertEqual(response.status_code, 401)

        # Test route with token
        response = self.app.delete('/bucketlists/1',
                                 headers={'token': self.get_token()})
        self.assertEqual(response.status_code, 204)

    def test_post_bucketlistitems_route(self):
        """Test that POST in /bucketlists/<>/items/ route is working"""
        bucketlist_item = json.dumps({"title": "Travel"})

        # Test route without token
        response = self.app.post('/bucketlists/1/items/', data=bucketlist_item)
        self.assertEqual(response.status_code, 401)

        # Test route with token
        response = self.app.post('/bucketlists/1/items/',
                                 data=bucketlist_item,
                                 headers={'token': self.get_token(),
                                          'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 201)


    def test_put_specific_bucketlistitem_route(self):
        """Test that PUT in /bucketlists/<>/items/<> route is working"""
        # Updated item
        bucketlist_item = json.dumps({"title": "I need to do Y"})

        # Test route without token
        response = self.app.put('/bucketlists/1/items/1', data=bucketlist_item)
        self.assertEqual(response.status_code, 401)

        # Test route with token
        response = self.app.put('/bucketlists/1/items/1',
                                 data=bucketlist_item,
                                 headers={'token': self.get_token(),
                                          'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['message'], "BucketlistItem #1 Successfully updated")

    def test_delete_specific_bucketlistitem_route(self):
        """Test that DELETE in /bucketlists/<>/items/<> route is working"""

        # Test route without token
        response = self.app.delete('/bucketlists/1/items/1')
        self.assertEqual(response.status_code, 401)

        # Test route with token
        response = self.app.delete('/bucketlists/1/items/1',
                                 headers={'token': self.get_token()})
        self.assertEqual(response.status_code, 204)
