"""sqlalchemy gamelog models for the Boardgame Shelf"""

from flask_sqlalchemy import SQLAlchemy

from user_models import db



class Playlog(db.Model):
    """stores a users gamelogs for game playthroughs"""

    __tablename__ = "playlogs"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False,)

    game_id = db.Column(db.Integer,
                        db.ForeignKey('games.id'),
                        nullable=False,)

    date_of_playthrough = db.Column(db.Date)

    player_count = db.Column(db.Integer,
                             nullable=False)

    notes = db.Column(db.Text)


class Player(db.Model):
    '''store's the player info for playlogs'''

    __tablename__ = "players"

    id = db.Column(db.Integer,
                   primary_key= True,
                   autoincrement= True,)
    
    player_name = db.Column(db.Text)

    playthroughs = db.relationship('Playthrough',
                                   backref='players')


class Playthrough(db.Model):
    '''many to many relationship between players and playlogs'''

    __tablename__ = "playthroughs"

    playlog_id = db.Column(db.Integer,
                           db.ForeignKey('playlogs.id'),
                           primary_key= True)
    
    player_id = db.Column(db.Integer,
                          db.ForeignKey('players.id'),
                          primary_key= True)
    
    player_score = db.Column(db.Integer,
                             default= 0)