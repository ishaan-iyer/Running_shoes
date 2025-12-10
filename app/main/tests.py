import os
import app # ensure routes/blueprints are registered
from unittest import TestCase

from datetime import date


from app.extensions import app as flask_app, db, bcrypt
from app.models import User, Shoe, Manufacturer


def create_user(username='me1', password='password'):
    """Create and return a test user."""
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, password=password_hash)
    db.session.add(user)
    db.session.commit()
    return user


def login(client, username='me1', password='password'):
    """Log in a user via the /login route."""
    login_data = {
        'username': username,
        'password': password
    }
    return client.post('/login', data=login_data, follow_redirects=True)


def create_manufacturer(name='Nike', country='USA'):
    """Create and return a test manufacturer."""
    m = Manufacturer(name=name, country=country)
    db.session.add(m)
    db.session.commit()
    return m


def create_shoe(
        name='Pegasus',
        model_year=2024,
        size=10,
        manufacturer=None,
        category=None,
):
    """Create and return a test shoe."""
    if manufacturer is None:
        manufacturer = create_manufacturer()


    shoe = Shoe(
        name=name,
        model_year=model_year,
        size=size,
        manufacturer=manufacturer,
        category=category  
    )
    db.session.add(shoe)
    db.session.commit()
    return shoe


class MainRouteTests(TestCase):
    """Tests for main blueprint routes (homepage, shoes, favorites)."""


    def setUp(self):
        """Executed prior to each test."""
        # Test config
        flask_app.config['TESTING'] = True
        flask_app.config['WTF-CSRF_ENABLED'] = False
        flask_app.config['DEBUG'] = False
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        self.ctx = flask_app.app_context()
        self.ctx.push()

        db.drop_all()
        db.create_all()

        self.app = flask_app.test_client()


    def tearDown(self):
        """Execcuted after each test."""
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_homepage_lists_shoes_and_manufacturers(self):
        """GET / should show shoes and manufacturers."""
        manufacturer = create_manufacturer(name='Nike', country='USA')
        shoe = create_shoe(name='Pegasus 41', manufacturer=manufacturer)


        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)


        response_text = response.get_data(as_text=True)
        self.assertIn('Pegasus 41', response_text)
        self.assertIn('Nike', response_text)

    def test_create_shoe_requires_login(self):
        """GET /create_shoe should redirect to login when not logged in."""
        response = self.app.get('/create_shoe', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        # Assuming your login template contains 'Log In'
        self.assertIn('Log In', response_text)

    def test_create_manufacturer_requires_login(self):
        """GET /create_manufacturer should redirect to login when not logged in."""
        response = self.app.get('/create_manufacturer', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


        response_text = response.get_data(as_text=True)
        self.assertIn('Log In', response_text)

    def test_shoe_detail_displays_shoe(self):
        """GET /shoe/<id> should show details for that shoe."""
        manufacturer = create_manufacturer(name='Adidas', country='Germany')
        shoe = create_shoe(
            name='Adios Pro',
            model_year=2023,
            size=9,
            manufacturer=manufacturer
        )


        response = self.app.get(f'/shoe/{shoe.id}')
        self.assertEqual(response.status_code, 200)


        response_text = response.get_data(as_text=True)
        self.assertIn('Adios Pro', response_text)
        self.assertIn('Model Year', response_text)
        self.assertIn('Size', response_text)