"""Home and Search View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest tests/test_playlog_views.py


import os
from unittest import TestCase

from user_models import db, connect_db, User
from playlog_models import Playlog, PlaySession


os.environ['DATABASE_URL'] = "postgresql:///boardgames_test"


from app import app, CURR_USER_KEY


db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False



class PlaylogViewTestCase(TestCase):

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.signup('test1', 'user1@email.com', 'password', None)
        u1id = 1111
        u1.id = u1id

        u2 = User.signup('test2', 'user2@eamil.com', 'password', None)
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
    

    def test_unauthorized_add_playlog(self):
         '''tests an unauthorized user attempting to add a playlog'''
        
         with self.client as c:
           
            resp = c.get('/playlogs/add_log/OIXt3DmJU0',  follow_redirects=True,)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('You must be logged in to record a playlog, please login or signup', html)



    def test_authorized_add_playlog(self):
        ''' tests an authorized user adding a playlog'''


        with self.client as c:
             with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id


        resp = c.post('/playlogs/add_log/Catan',  follow_redirects=True,)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<th scope="col">Score</th>', html)


    def test_unauthorized_remove_playlog(self):
         """tests an unauthorizded user attempting to remove a playlog"""

         pl = Playlog(id=1,user_id=self.u1.id,player_count=2)
         db.session.add(pl)
         db.session.commit()

         with self.client as c:
           
            resp = c.post('/playlogs/remove_log/1',  follow_redirects=True,)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Access unauthorized.', html)



    def test_authorized_remove_playlog(self):
        """tests an authorized user removing a playlog"""

        pl = Playlog(id=1,user_id=self.u1.id,player_count=2)
        db.session.add(pl)
        db.session.commit()

        with self.client as c:
             with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id

        resp = c.post('/playlogs/remove_log/1',  follow_redirects=True,)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(' display-5 sitefont mt-5">No playlogs currently added, click', html)