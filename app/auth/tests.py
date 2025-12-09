import os
import app  # ensure routes/blueprints are registered
from unittest import TestCase

from datetime import date
 
from app.extensions import app as flask_app, db, bcrypt
from app.models import User


def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()


#################################################
# Tests
#################################################

class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""
 
    def setUp(self):
        """Executed prior to each test."""
        # Test config
        flask_app.config['TESTING'] = True
        flask_app.config['WTF_CSRF_ENABLED'] = False
        flask_app.config['DEBUG'] = False
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        # 1. Push an application context
        self.ctx = flask_app.app_context()
        self.ctx.push()

        # 2. Reset the database for each test
        db.drop_all()
        db.create_all()

        # 3. Create a test client
        self.app = flask_app.test_client()

    def tearDown(self):
        """Executed after each test."""
        db.session.remove()
        db.drop_all()
        # Pop the application context
        self.ctx.pop()

    def test_signup(self):

        post_data = {
            'username': 'newuser',
            'password': 'password'
        }
        response = self.app.post('/signup', data=post_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        created_user = User.query.filter_by(username='newuser').one()
        self.assertIsNotNone(created_user)

    def test_signup_existing_user(self):

        create_user()

        post_data = {
            'username': 'me1',
            'password': 'password'
        }
        response = self.app.post('/signup', data=post_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        # This must match your template:
        # <li class="error">That username is taken. Please choose a different one.</li>
        self.assertIn('That username is taken. Please choose a different one.', response_text)

    def test_login_correct_password(self):

        create_user()

        post_data = {
            'username': 'me1',
            'password': 'password'
        }
        response = self.app.post('/login', data=post_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertNotIn('Log In', response_text)

    def test_login_nonexistent_user(self):

        post_data = {
            'username': 'ghostuser',
            'password': 'password'
        }
        response = self.app.post('/login', data=post_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('No user with that username', response_text)
        self.assertIn('Log In', response_text)

    def test_login_incorrect_password(self):

        create_user()

        post_data = {
            'username': 'me1',
            'password': 'wrongpassword'
        }
        response = self.app.post('/login', data=post_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        # Template shows: Password doesn&#39;t match. Please try again.
        # Matching the literal HTML-escaped string:
        self.assertIn("Password doesn&#39;t match. Please try again.", response_text)
        self.assertIn('Log In', response_text)

    def test_logout(self):
        create_user()

        login_data = {
            'username': 'me1',
            'password': 'password'
        }
        self.app.post('/login', data=login_data, follow_redirects=True)

        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Log In', response_text)
