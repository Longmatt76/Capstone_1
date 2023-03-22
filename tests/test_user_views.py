"""User Views tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest tests/test_user_views.py


from app import app, CURR_USER_KEY
import os
from unittest import TestCase

from user_models import db, connect_db, User
from game_models import GameCollection, Wishlist
from playlog_models import Playlog, PlaySession


os.environ['DATABASE_URL'] = "postgresql:///boardgames_test"


db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):

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

    def test_show_collection(self):
        """tests the users collection view"""

        g1 = GameCollection(user_id=self.u1.id, game_id=1111, name='testgame1')
        g2 = GameCollection(user_id=self.u1.id, game_id=2222, name='testgame2')

        games = [g1, g2]
        db.session.add_all(games)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id

        resp = c.get(f'/users/{self.u1.id}/game_collection')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('testgame1', html)
        self.assertIn('testgame2', html)
        self.assertIn(
            '<h5 class="modal-title">Edit Rating: testgame1</h5>', html)

   
    def test_show_wishlist(self):
        """tests the users wishlist view"""

        g1 = Wishlist(user_id=self.u1.id, game_id=1111, name='wishgame1')
        g2 = Wishlist(user_id=self.u1.id, game_id=2222, name='wishgame2')

        wishes = [g1, g2]
        db.session.add_all(wishes)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id

        resp = c.get(f'/users/{self.u1.id}/wishlist')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('wishgame1', html)
        self.assertIn('wishgame2', html)
        self.assertIn('Price alert subcription status: wishgame1</h5>', html)

    
    def test_show_playlogs(self):
        """tests the view for a users playlogs"""

        p1 = Playlog(id=1, user_id=self.u1.id, player_count=3)
        db.session.add(p1)
        db.session.commit()

        ps1 = PlaySession(player_id=1, playlog_id=1,
                          player_name='Testuser1', player_score='10')
        ps2 = PlaySession(player_id=2, playlog_id=1,
                          player_name='Testuser2', player_score='20')
        ps3 = PlaySession(player_id=2, playlog_id=1,
                          player_name='Testuser3', player_score='30')

        sessions = [ps1, ps2, ps3]
        db.session.add_all(sessions)

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id

        resp = c.get(f'/users/{self.u1.id}/playlogs')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<th scope="col">Player #</th>', html)
        self.assertIn('Playlogs', html)
        self.assertIn('<th scope="col">Score</th>', html)

  
    def test_show_user_profile(self):
        """ tests the users profile view """

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id

        resp = c.get(f'/users/{self.u1.id}/profile')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('test1', html)
        self.assertIn('user1@email.com', html)
        self.assertIn('<a href="/users/1111/delete">', html)

   
    def test_edit_user_profile(self):
        """tests editing a users profile"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id

        # incorrect password
        resp = c.post(
            f"/users/{self.u1.id}/update",
            data={"username": "new_username", "password": "wrong_password"},
            follow_redirects=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Access unauthorized, please reenter password", str(resp.data))
        u = User.query.get(self.u1.id)
        self.assertNotEqual(u.username, "new_username")

        # success case
        resp = c.post(
            f"/users/{self.u1.id}/update",
            data={"username": "new_user", "password": "password"},
            follow_redirects=True,
        )
        self.assertEqual(resp.status_code, 200)
        u = User.query.get(self.u1.id)
        self.assertEqual(u.username, "new_user")

    
    def test_delete_user(self):
        """Does route delete current user and log them out?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id

            resp = c.post(f"/users/{self.u1.id}/delete",
                          data={'username': 'test1', 'password': 'password'}, 
                          follow_redirects=True)
           
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Sorry to see you go, rejoin anytime!", str(resp.data))
            u = User.query.get(self.u1.id)
            self.assertIsNone(u)
           
