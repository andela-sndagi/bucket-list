import json

import unittest

from ..app.models import User, initialise, drop, app


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
            'username': 'username',
            'password': 'p@ssw0rd'
        })
        response = self.app.post('/auth/register/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = json.dumps({
            'username': 'username',
            'password': 'p@ssw0rd',
            'conf_password': 'password'
        })
        response = self.app.post('/auth/register/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = json.dumps({
            'username': 'username',
            'password': 'p@ssw0rd',
            'conf_password': 'p@ssw0rd'
        })
        response = self.app.post('/auth/register/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)


    # def test_post_login_route(self):
    #     """Test POST in /auth/login/ route"""

    #     """First Register"""
    #     data = json.dumps({
    #         'username': 'username',
    #         'password': 'password',
    #         'conf_password': 'password'
    #     })
    #     response = self.app.post('/auth/register/', data=data, content_type='application/json')
    #     self.assertEqual(response.status_code, 201)

    #     """Then Login"""
    #     l_data = json.dumps({
    #         "username": "username",
    #         "password": "password"
    #     })
    #     import ipdb; ipdb.set_trace()
    #     response = self.app.post('/auth/login/', data=l_data, content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
