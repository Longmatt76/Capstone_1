"""Home and Search View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest tests/test_collection_views.py


import os
from unittest import TestCase

from user_models import db, connect_db, User
from game_models import GameCollection


os.environ['DATABASE_URL'] = "postgresql:///boardgames_test"


from app import app, CURR_USER_KEY


db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False



class CollectionViewTestCase(TestCase):

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
    

    def test_unauthorized_addgame_collection(self):
        """test's an unauthorized user attempting to add game to a collection"""
        
        with self.client as c:
           
            resp = c.get('/gamecollection/add_game/OIXt3DmJU0',  follow_redirects=True,)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('You must be logged in to add a game to your collection', html)


    def test_authorized_addgame_collection(self):
        """test's an authorized user attempting to add game to a collection"""
        
        with self.client as c:
             with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id
           
        resp = c.get('/gamecollection/add_game/OIXt3DmJU0',  follow_redirects=True,)
        html = resp.get_data(as_text=True)
            
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h5 class="modal-title">Edit Rating: Catan</h5>', html)


    def test_unauthorized_removegame_collection(self):
        """test's an unauthorized user attempting to remove game from a collection"""
        
        with self.client as c:
           
            resp = c.get('/gamecollection/remove_game/OIXt3DmJU0',  follow_redirects=True,)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Access unauthorized.', html)


    def test_authorized_removegame_collection(self):
        """test's an authorized user attempting to remove game from a collection"""
        
        with self.client as c:
             with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id

        g1 = GameCollection(user_id=self.u1.id,game_id='OIXt3DmJU0',name='Catan')
        db.session.add(g1)
        db.session.commit()
           
        resp = c.get('/gamecollection/remove_game/OIXt3DmJU0',  follow_redirects=True,)
        html = resp.get_data(as_text=True)
            
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn('<h5 class="modal-title">Edit Rating: Catan</h5>', html)


    def test_edit_rating(self):
        """tests a user editing a rating for a game in thier collection"""
        
        with self.client as c:
             with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id

        g1 = GameCollection(user_id=self.u1.id,game_id='OIXt3DmJU0',name='Catan')
        db.session.add(g1)
        db.session.commit()

        resp = c.post('/gamecollection/edit_rating/OIXt3DmJU0', data={'rating': 5})
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<option>5  &nbsp;"so so"', html)


    def test_edit_comment(self):
        """tests a user editing a comment for a game in thier collection"""
        
        with self.client as c:
             with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id

        g1 = GameCollection(user_id=self.u1.id,game_id='OIXt3DmJU0',name='Catan')
        db.session.add(g1)
        db.session.commit()

        resp = c.post('/gamecollection/edit_comments/OIXt3DmJU0', data={'comment': 'sheep and wood'})
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('sheep and wood', html)


    def test_value_game(self):
        '''tests a user valuing a game in thier collection'''

        with self.client as c:
             with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id

        g1 = GameCollection(user_id=self.u1.id,game_id='OIXt3DmJU0',name='Catan')
        db.session.add(g1)
        db.session.commit()

        resp = c.get('/gamecollection/value_game/OIXt3DmJU0', follow_redirects=True,)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('$', html)
