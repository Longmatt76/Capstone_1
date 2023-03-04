"""Wishlist model tests."""

# run these tests like: python -m unittest tests/test_wishlist_model.py


from app import app
import os
from unittest import TestCase


from user_models import db, User, Game, Wishlist

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
