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
        # Add configuration to the app
        app.config.update({'TESTING': True, 'SECRET_KEY': "abcdefgh"})
        self.app = app.test_client()
        initialise()

    def tearDown(self):
        """Tearing down after tests"""
        print "=> Tearing down after tests"
        drop()

    def test_post_register_route(self):
        """Test POST in /auth/register/ route"""

        # Testing that 'conf_password' not entered
        data = json.dumps({
            'username': 'user',
            'password': 'p@ssw0rd'
        })
        response = self.app.post('/auth/register/', data=data,
            content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Testing that 'conf_password' is incorrect
        data = json.dumps({
            'username': 'user',
            'password': 'p@ssw0rd',
            'conf_password': 'password'
        })
        response = self.app.post('/auth/register/', data=data,
            content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Correct entry
        data = json.dumps({
            'username': 'user',
            'password': 'p@ssw0rd',
            'conf_password': 'p@ssw0rd'
        })
        response = self.app.post('/auth/register/', data=data,
            content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(User.query.all(), None)
        self.assertEqual(len(User.query.all()), 1)

        # Testing that there is a user with that username
        data = json.dumps({
            'username': 'user',
            'password': 'p@ssw0rd',
            'conf_password': 'p@ssw0rd'
        })
        response = self.app.post('/auth/register/', data=data,
            content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_login_route(self):
        """Test POST in /auth/login/ route"""

        # Testing that there's no user by that username
        data = json.dumps({
            'username': 'user',
            'password': 'p@ssw0rd'
        })
        response = self.app.post('/auth/login/', data=data,
            content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Create user
        user = User(username='username', password='p@ssw0rd')
        db.session.add(user)
        db.session.commit()

        # Testing that there's a wrong password entry
        data = json.dumps({
            'username': 'username',
            'password': 'password'
        })
        response = self.app.post('/auth/login/', data=data,
            content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Correct entry
        data = json.dumps({
            'username': 'username',
            'password': 'p@ssw0rd'
        })
        response = self.app.post('/auth/login/', data=data,
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
