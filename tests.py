import unittest
import app


class AppTestCase(unittest.TestCase):
    """docstring for AppTestCase"""
    def setUp(self):
        print('=> Setting up the environment for testing')
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def tearDown(self):
        print('=> Tearing down after tests')

    # Test if the index page is working
    def test_api_index(self):
        resp = self.app.get('/')
        assert "200 OK" == resp.status
        assert "Bucket List Service API is ready" in resp.data

if __name__ == '__main__':
    unittest.main()
