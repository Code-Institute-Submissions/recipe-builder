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
        
    def _insert_user(self, username, password, role_name):
        """Set up test User"""
        test_role = Role(role_name)
        mongo.db.session.add(test_role)
        mongo.db.session.commit()
        
        test_user = User(username)
        test.user.set_password(password)
        mongo.db.session.add(test_user)
        mongo.db.session.commit()
        
    def test_login(self):
        """Tests if the login form works correctly"""
        result = self.client.post('/login', data=dict (
            username='test',
            password='test'
        ), follow_redirects=True)
            
        self.assertEqual(result.status_code, 200)
        self.assertIn('You have been logged in', result.data)
        
    def test_failed_login(self):
        """Tests a failed login form works correctly"""
        self._insert_user('test', 'test', 'default')
        result = self.client.post('/login', data=dict(
            username='test',
            password='badpassword'
        ), follow_redirect=True)
        
        self.assertEqual(result.status.code, 200)
        self.assertIn('Invalid username/password combination', result.data)
        result = self.client.get('/index')
        self.assertEqual(result.status_code, 403)

if __name__ == '__main__':
    unittest.main()