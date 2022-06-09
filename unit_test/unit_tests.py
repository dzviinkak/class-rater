import sys

sys.path.append('.')
sys.path.append('..')

from web import app, db
import unittest

class PageNavigationTests(unittest.TestCase):
    def test_index(self):
        test_client = app.test_client(self)
        response = test_client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)


    def test_login(self):
        test_client = app.test_client(self)
        response = test_client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)


    def test_register(self):
        test_client = app.test_client(self)
        response = test_client.get('/register', content_type='html/text')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()