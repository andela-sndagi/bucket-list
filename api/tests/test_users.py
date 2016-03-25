import json
import unittest

from ..app.models import User, initialise, drop, app, db


class AppTestCase(unittest.TestCase):
    """
    AppTestCase
    """

    def setUp(self):
        """Setting up the environment for testing"""
        print "=> Setting up the environment for testing"
        self.app = app.test_client()
        initialise()

    def tearDown(self):
        """Tearing down after tests"""
        print "=> Tearing down after tests"
        drop()

    def test_post_register_route(self):
        """Test POST in /auth/register/ route"""

        data = json.dumps({
            'username': 'user',
            'password': 'p@ssw0rd'
        })
        response = self.app.post('/auth/register/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = json.dumps({
            'username': 'user',
            'password': 'p@ssw0rd',
            'conf_password': 'password'
        })
        response = self.app.post('/auth/register/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = json.dumps({
            'username': 'user',
            'password': 'p@ssw0rd',
            'conf_password': 'p@ssw0rd'
        })
        response = self.app.post('/auth/register/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(User.query.all(), None)

    def test_post_login_route(self):
        """Test POST in /auth/login/ route"""

        data = json.dumps({
            'username': 'user',
            'password': 'p@ssw0rd'
        })
        response = self.app.post('/auth/login/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)

        user = User(username='username', password='p@ssw0rd')
        db.session.add(user)
        db.session.commit()
        data = json.dumps({
            'username': 'username',
            'password': 'p@ssw0rd'
        })
        response = self.app.post('/auth/login/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
