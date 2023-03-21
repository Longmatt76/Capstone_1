"""sqlalchemy gamelog models for the Boardgame Shelf"""

from flask_sqlalchemy import SQLAlchemy
from user_models import db



class Playlog(db.Model):
    """stores a users playlogs for game playthroughs"""

    __tablename__ = "playlogs"

    id = db.Column(db.Integer,
                   primary_key=True,
                   unique=True,
                   autoincrement=True,)
 
   
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='CASCADE'),
                        nullable=False,)

    game = db.Column(db.Text)

    date_of_playthrough = db.Column(db.Date)

    player_count = db.Column(db.Integer,
                             nullable=False)
    
    location = db.Column(db.Text)

    notes = db.Column(db.String(140))

    sessions = db.relationship('PlaySession',
                              backref= 'playlogs')
    



    


class PlaySession(db.Model):
    '''many to many connection between players and playlogs'''

    __tablename__ = "play_sessions"
    
    player_id = db.Column(db.Integer,
                          primary_key= True,
                          autoincrement=True)
    
    
    playlog_id = db.Column(db.Integer,
                           db.ForeignKey('playlogs.id', ondelete='CASCADE'),
                           primary_key= True)

    player_name = db.Column(db.Text)

    
    player_score = db.Column(db.Integer,
                             default= 0)