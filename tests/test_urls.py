import unittest
import re

from flask_pymongo import PyMongo

import app as app_module

app = app_module.app

"""Disable CSRF checks and Set up test Database on MondoDB"""
app.config["TESTING"] = True
app.config["WTF_CSRF_ENABLED"] = False
app.config["MONGO_URI"] = 'mongodb://localhost:27017/loveFoodTesting'

mongo = PyMongo(app)
app_module.mongo = mongo


class TestURLs(unittest.TestCase):
    def setUp(self):
        """Work around bugs, Flask Admin, Flask Restful extensions and Flask SQLAlchemy initialiser"""
        self.client = app.test_client()
        mongo.db.app = app
        mongo.db.create_all()
        
    def tearDown(self):
        """Destroys any objects created in setUp method that cannot automatically be deleted or closed"""
        mongo.db.session.remove()
        
    def test_root_redirect(self):
        """Tests if the root URL gives a 302"""
        result = self.client.get('/')
        assert result.status_code == 302
        assert "/index/" in result.header ['Home Page']
        
    def test_recipe_home(self):
        """Tests if the recipe page returns successfully"""
        result = self.client.get('/get_recipes/')
        self.assertEqual (result.status_code, 200)

if __name__ == '__main__':
    unittest.main()