import unittest
from app import app, db
from models import User
from flask_sqlalchemy import SQLAlchemy


# Use a test database for testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False


# Create a test case class
class BloglyTestCase(unittest.TestCase):


    def setUp(self):
        # Set up the test client, application context, and create the test database
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()


    def tearDown(self):
        # Clean up after each test: remove the session and drop the test database
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    # Test the '/' route
    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  
        # Expect a redirect


    # Test the '/users' route
    def test_users_index_route(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)  
        # Expect a successful response


    # Test the '/users/new' route (form)
    def test_users_new_form_route(self):
        response = self.client.get('/users/new')
        self.assertEqual(response.status_code, 200)  
        # Expect a successful response


    # Test the '/users/new' route (create a new user)
    def test_users_new_route(self):
        user_data = {
            'first_name': 'Mitao',
            'last_name': 'Cat',
            'image_url': 'https://example.com/mitaocat.jpg'
        }
        response = self.client.post('/users/new', data=user_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)  
        # Expect a successful response
        self.assertTrue(User.query.filter_by(first_name='Mitao').first())  
        # Expect the user to be in the database


# Run the tests
if __name__ == '__main__':
    unittest.main()
