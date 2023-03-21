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


    def test_home_page(self):
        """test the status code and html displayed on the homepage"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id


            resp = c.get('/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(' <title>The Boardgame Shelf</title>', html)



    def test_search(self):
        '''tests sending a search query'''

        with app.test_client() as client:
            resp = client.get('/search?search=catan')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h5 class="card-title">Catan</h5>', html)



    def test_show_gmdetails(self):
        """tests a user clicking on a game returned from a search 
        query which sends an api request for details of that game and displays the details """

        with app.test_client() as client:
            resp = client.get('/search/OIXt3DmJU0/game_details')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<span class="text-info gt_span"> (1995)</span>', html)
            self.assertIn('<td class="text-light">45-90</td>', html)
            self.assertIn(' Hills produce brick, forests produce lumber, mountains produce ore, fields produce grain', html)





