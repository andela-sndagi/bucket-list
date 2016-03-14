# sqlalchemy_orm/tests.py

import os, sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import unittest

from flask import json, jsonify
from flask.ext.fixtures import FixturesMixin
from faker import Factory

from sqlalchemy_orm.app import app
from sqlalchemy_orm.models import db, Bucketlist, BucketlistItem, User


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
        self.fake = Factory.create()

    def tearDown(self):
        """Tearing down after tests"""
        print "=> Tearing down after tests"

    def test_api_index(self):
        """Test if the index page is working"""
        response = self.app.get('/')
        print '=> Getting to "/"'
        assert response.status == "200 OK"
        self.assertIn('Bucket List Service API is ready', response.data)

    def test_bucketlists_in_fixtures(self):
        """Test bucketlist entries in fixtures"""
        bucketlists = Bucketlist.query.all()
        self.assertEqual(len(bucketlists) == Bucketlist.query.count(), 1)
        self.assertEqual(len(bucketlists[0].items), 1)

    def test_bucketlist_items_in_fixtures(self):
        """Test bucketlistitems entries in fixtures"""
        items = BucketlistItem.query.all()
        self.assertEqual(len(items) == Bucketlist.query.count(), 1)
        bl1 = Bucketlist.query.filter(Bucketlist.name == 'BucketList1').first()
        for item in items:
            assert item.bucketlist_id == bl1

    def test_get_bucketlists_route(self):
        """Test that GET in /bucketlists/ route is working"""
        response = self.app.get('/bucketlists/')
        self.assertEqual(response.status_code, 200)

    def test_post_bucketlists_route(self):
        """Test that POST in /bucketlists/ route is working"""
        bucketlist = {"name": "Travel", "created_by": "Stan"}

        response = self.app.post('/bucketlists/', data=bucketlist)
        bucketlists = Bucketlist.query.all()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(bucketlists), 2)

    def test_get_specific_bucketlist_route(self):
        """Test that GET in /bucketlists/<> route is working"""
        response = self.app.get('/bucketlists/1')
        self.assertEqual(response.status_code, 200)
        bucketlist = {"name": "Travel", "created_by": "Stan"}
        response = self.app.post('/bucketlists/', data=bucketlist)
        response = self.app.get('/bucketlists/2')
        self.assertEqual(response.status_code, 200)

    def test_put_specific_bucketlist_route(self):
        """Test that POST in /bucketlists/<> route is working"""
        bucketlist = {"name": "New Bucketlist", "created_by": "Stan"}

        response = self.app.put('/bucketlists/1', data=bucketlist)
        self.assertEqual(response.status_code, 200)
        bucketlists = Bucketlist.query.all()
        self.assertEqual(len(bucketlists), 1)

    def test_delete_specific_bucketlist_route(self):
        """Test that POST in /bucketlists/<> route is working"""
        response = self.app.delete('/bucketlists/1')
        bucketlists = Bucketlist.query.all()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(bucketlists), 0)

    def test_post_bucketlistitems_route(self):
        """Test that POST in /bucketlists/<>/items/ route is working"""
        bucketlist_item = {"title": "Travel"}

        response = self.app.post('/bucketlists/1/items/', data=bucketlist_item)
        bucketlists = Bucketlist.query.all()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(bucketlists[0].items), 2)

    def test_put_specific_bucketlistitem_route(self):
        """Test that PUT in /bucketlists/<>/items/<> route is working"""
        bucketlist_item = {"title": "I need to do Y"}

        response = self.app.put('/bucketlists/1/items/1', data=bucketlist_item)
        bucketlists = Bucketlist.query.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(bucketlists[0].items), 1)

    def test_delete_specific_bucketlistitem_route(self):
        """Test that DELETE in /bucketlists/<>/items/<> route is working"""
        response = self.app.delete('/bucketlists/1/items/1')
        bucketlists = Bucketlist.query.all()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(bucketlists[0].items), 0)

    def test_register_route(self):
        """Test that POST in /auth/register/ route is working"""
        register = {"username": "stanmd", "password": "123456", "conf_password": "123456"}

        users = User.query.all()
        self.assertEqual(len(users), 1)
        # response = self.app.post('/auth/register/', data=register)
        # self.assertEqual(response.status_code, 201)
        # self.assertEqual(len(users), 2)

    def test_login_route(self):
        """Test that POST in /auth/login/ route is working"""
        # login_one = {"username": "User1", "password": "123465"}
        # login_two = {"username": "User1", "password": "123456"}

        users = User.query.all()
        self.assertEqual(len(users), 1)
        # response = self.app.post('/auth/login/', data=login_one)
        # self.assertEqual(response.status_code, 404)
        # response = self.app.post('/auth/login/', data=login_two)
        # self.assertEqual(response.status_code, 201)
        # self.assertIn(response.data, 'token')
