"""Gamelog model tests."""

# run these tests like: python -m unittest tests/test_playlog_models.py


from app import app
import os
from unittest import TestCase
from playlog_models import Playlog, PlaySession


from user_models import db, User

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



    def test_playlog_model(self):
        '''does basic model work?'''

        pl1 = Playlog(id=1,user_id=self.u1.id,game='testgame1',player_count=4)
        pl2 = Playlog(id=2,user_id=self.u1.id,game='testgame2',player_count=6)
        pl3 = Playlog(id=3,user_id=self.u1.id,game='testgame3',player_count=2)
        pl4 = Playlog(id=4,user_id=self.u2.id,game='testgame4',player_count=7, notes='testing mctestine')

        playlogs = [pl1,pl2,pl3,pl4]
        db.session.add_all(playlogs)
        db.session.commit()
        
        self.assertEqual(len(self.u1.playlogs), 3)
        self.assertEqual(len(self.u2.playlogs), 1)
        self.assertEqual(self.u1.playlogs[0].player_count, 4)
        self.assertEqual(self.u1.playlogs[1].player_count, 6)
        self.assertEqual(self.u2.playlogs[0].player_count, 7)
        self.assertNotEqual(self.u2.playlogs[0].notes,'not testing mctestine')



    def test_playsession_model(self):
         """does the basic model work? """
         
         p1 = Playlog(id=1,user_id=self.u1.id,game='testgame1',player_count=3)
         db.session.add(p1)
         db.session.commit()

         ps1 = PlaySession(player_id=1,playlog_id=1,player_name='test1',player_score=10)
         ps2 = PlaySession(player_id=2,playlog_id=1,player_name='test2',player_score=20)
         ps3 = PlaySession(player_id=3,playlog_id=1,player_name='test3',player_score=30)

         playsessions = [ps1,ps2,ps3]
         db.session.add_all(playsessions)
         db.session.commit()


         self.assertEqual(p1.user_id, self.u1.id)
         self.assertEqual(p1.game, 'testgame1')
         self.assertEqual(ps1.player_name,'test1')
         self.assertNotEqual(ps2.player_score, 300)




