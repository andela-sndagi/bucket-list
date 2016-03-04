import unittest
import app
from app import models


class AppTestCase(unittest.TestCase):
    """App TestCase"""
    def setUp(self):
        """Setting up the environment for testing"""
        print('=> Setting up the environment for testing')
        self.app = app.app.test_client()
        models.initialize_db()

    def tearDown(self):
        """Tearing down after tests"""
        print('=> Tearing down after tests')
        models.db.close()

    def test_api_index(self):
        """Test if the index page is working"""
        response = self.app.get('/')
        print('=> Getting to "/"')
        assert "200 OK" == response.status
        self.assertIn ('Bucket List Service API is ready', response.data)

if __name__ == '__main__':
    unittest.main()
