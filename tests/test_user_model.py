"""User model tests."""

# run these tests like: python -m unittest tests/test_user_model.py


from app import app
import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Gamelog

os.environ['DATABASE_URL'] = "postgresql:///boardgames_test"


db.create_all()


class UserModelTestCase(TestCase):

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.signup('test1', 'user1@email.com', 'password', None)
        u1id = 1111
        u1.id = u1id

        u2 = User.signup('test2', 'user2@eamil.com','password',None)
        u2id = 2222
        u2.id = u2id

        db.session.commit()

        u1 = User.query.get(u1id)
        u2 = User.query.get(u2id)

        self.u1 = u1
        self.u2 = u2
       
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    
    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no gamelogs
        self.assertEqual(len(u.gamelogs), 0)

       
        """tests for signup"""
    def test_signup_success(self):
        u3 = User.signup(username='user3', email='user3@email.com',
                         password='password', image_url=None)
        u3id = 3333
        u3.id = u3id

        db.session.commit()

        u3 = User.query.get(u3id)
        self.assertEqual(u3.username, 'user3')
        self.assertEqual(u3.email, 'user3@email.com')
        self.assertNotEqual(u3.password, 'password')
        self.assertTrue(u3.password.startswith('$2b$'))

  
    def test_signup_failure(self):
        u4 = User.signup(username=None, email='user4@email.com',
                         password='password', image_url=None)
        u4id = 4444
        u4.id = u4id
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

        
        '''tests for authentication'''
    def test_valid_authenticaion(self):
        u = User.authenticate(self.u1.username, 'password')
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.u1.id)

    
    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.password, 'notpassword'))
