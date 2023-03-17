"""sqlalchemy gamelog models for the Boardgame Shelf"""

from flask_sqlalchemy import SQLAlchemy
from user_models import db



class Playlog(db.Model):
    """stores a users playlogs for game playthroughs"""

    __tablename__ = "playlogs"

    id = db.Column(db.Integer,
                   primary_key=True,
                   unique=True,)
    
   
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False,)
    
    game_id = db.Column(db.Text, 
                        primary_key=True)

    date_of_playthrough = db.Column(db.Date)

    player_count = db.Column(db.Integer,
                             nullable=False)
    
    location = db.Column(db.Text)

    notes = db.Column(db.String(140))



class Player(db.Model):
    '''stores the info for the various players in the playlogs including their results'''

    __tablename__ = "players"
    
    player_id = db.Column(db.Integer,
                          primary_key= True)
    
    playlog_id = db.Column(db.Integer,
                           db.ForeignKey('playlogs.id'),
                           primary_key= True)

    player_name = db.Column(db.Text)


    player_score = db.Column(db.Integer,
                             default= 0)