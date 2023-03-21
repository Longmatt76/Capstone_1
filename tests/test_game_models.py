"""Game model tests."""

# run these tests like: python -m unittest tests/test_game_models.py


from app import app
import os
from unittest import TestCase


from user_models import db, User
from game_models import GameCollection,Wishlist

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



    def test_gamecollection_model(self):
        """Does basic model work?"""
        
        g1 = GameCollection(user_id=self.u1.id,game_id=1111,name='testgame1')
        g2 = GameCollection(user_id=self.u1.id,game_id=2222,name='testgame2')
        g3 = GameCollection(user_id=self.u2.id,game_id=3333,name='testgame3')
        games_to_add = [g1,g2,g3]
        db.session.add_all(games_to_add)
        db.session.commit()

        
        self.assertEqual(len(self.u1.games), 2)
        self.assertEqual(len(self.u2.games),1)
        self.assertEqual(self.u1.games[1].name,'testgame2')
        self.assertEqual(self.u2.games[0].name,'testgame3')
        self.assertNotEqual(self.u1.games[0].name, 'glergle')
        

    
    def test_wishlist_model(self):
        """Does basic model work?"""
        
        w1 = Wishlist(user_id=self.u1.id,game_id=1111,name='testgame1')
        w2 = Wishlist(user_id=self.u1.id,game_id=2222,name='testgame2')
        w3 = Wishlist(user_id=self.u2.id,game_id=3333,name='testgame3')
        wishes_to_add = [w1,w2,w3]
        db.session.add_all(wishes_to_add)
        db.session.commit()

        
        self.assertEqual(len(self.u1.wishes), 2)
        self.assertEqual(len(self.u2.wishes),1)
        self.assertEqual(self.u1.wishes[1].name,'testgame2')
        self.assertEqual(self.u2.wishes[0].name,'testgame3')
       


    