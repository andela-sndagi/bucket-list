import unittest
import app
import models
import config


class AppTestCase(unittest.TestCase):
    """App TestCase"""
    def setUp(self):
        """Setting up the environment for testing"""
        print('=> Setting up the environment for testing')
        self.app = app.app.test_client()
        import ipdb; ipdb.set_trace()
        models.initialize_db()

    def tearDown(self):
        """Tearing down after tests"""
        print('=> Tearing down after tests')
        models.db.close()

    def test_api_index(self):
        """Test if the index page is working"""
        response = self.app.get('/')
        assert "200 OK" == response.status
        assert "Bucket List Service API is ready" in response.data

    def test_db_creation_and_connection(self):
        """Test if the db is created and connected to"""
        response = self.app.
        # Beacause the db is created

if __name__ == '__main__':
    unittest.main()
