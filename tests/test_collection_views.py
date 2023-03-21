"""Home and Search View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest tests/test_home_search_views.py


import os
from unittest import TestCase

from user_models import db, connect_db, User


os.environ['DATABASE_URL'] = "postgresql:///boardgames_test"


from app import app, CURR_USER_KEY


db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False



class HomeViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()