import unittest
from flask_environments import Environments
from app import app
from app.models import db, initialize_db
from config import CONFIG


class AppTestCase(unittest.TestCase):
    """App TestCase"""

    def setUp(self):
        """Setting up the environment for testing"""
        print "=> Setting up the environment for testing"
        # Configure the app with the testing configuration
        self.app = app.test_client()
        env = Environments(app)
        env.from_object(CONFIG['testing'])
        initialize_db()
        db.connect()


    def tearDown(self):
        """Tearing down after tests"""
        print "=> Tearing down after tests"
        db.close()


    def test_api_index(self):
        """Test if the index page is working"""

        response = self.app.get('/')
        print '=> Getting to "/"'
        assert response.status == "200 OK"
        self.assertIn('Bucket List Service API is ready', response.data)

    def test_get_bucketlists(self):
        """Test if the /bucketlists/ endpoint"""
        response = self.app.get('/bucketlists/')
        print '=> Getting to "/bucketlists/"'
        assert response.status == "200 OK"
        # self.assertEqual([], response.data)

    def test_get_bucketlists_items(self):
        """Test if the /bucketlists/ endpoint"""
        response = self.app.get('/bucketlists/1/items/')
        print '=> Getting to "/bucketlists/<>/items/"'
        assert response.status == "200 OK"
        # self.assertEqual([], response.data)

if __name__ == '__main__':
    unittest.main()
