import unittest
import app as app_module

from flask_pymongo import PyMongo

app = app_module.app

#Config test DB on Mongo
app.config["TESTING"] = True
app.config["MONGO_URI"] = 'mongodb://localhost:27017//testing'


class TestUrls(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    
    def tearDown(self):
        pass
    
    def test_index(self):
        """Test Home Page loading"""
        result = self.client.get('/')
        assert result.status == '200 OK'

if __name__ == '__main__':
    unittest.main()