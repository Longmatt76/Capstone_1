"""sqlalchemy game models for the Boardgame Shelf"""

from flask_sqlalchemy import SQLAlchemy
from user_models import db



class Game(db.Model):
    """stores detailed game data in the db"""

    __tablename__ = 'games'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,)

    api_handle = db.Column(db.Text,
                           nullable=False,
                           unique=True,)

    name = db.Column(db.Text,
                     nullable=False,
                     unique=True,)

    year_published = db.Column(db.Integer)

    description = db.Column(db.Text)

    thumb_url = db.Column(db.Text)

    image_url = db.Column(db.Text)
    
    primary_designer = db.Column(db.Text)

    players = db.Column(db.Text)

    playtime = db.Column(db.Text)

    rules_url = db.Column(db.Text)

    offical_url = db.Column(db.Text)

    estimated_value = db.Column(db.Integer)

    def __repr__(self):
        return f"<Game #{self.id}: {self.api_handle}, {self.name}>"


class Mechanic(db.Model):
    """stores the api data for a games mechanics"""

    __tablename__ = "mechanics"

    id = db.Column(db.TEXT,
                   primary_key=True)

    name = db.Column(db.Text,
                     nullable=False)

    url = db.Column(db.Text)


class GameMechanic(db.Model):
    """many to many relationship between a game and it's mechanics"""

    __tablename__ = "game_mechanics"

    id = db.Column(db.Integer,
                   primary_key=True)
    
    game_id = db.Column(db.Integer,
                   db.ForeignKey('games.id'))
    
    mech_id = db.Column(db.Text,
                    db.ForeignKey('mechanics.id'))


class Category(db.Model):
    """stores the api data for a games categories"""

    __tablename__ = "categories"

    id = db.Column(db.Text,
                   primary_key=True)

    name = db.Column(db.Text,
                     nullable=False)

    url = db.Column(db.Text)



class GameCategory(db.Model):
    """Many to many relationship between a game and it's mechanics"""

    __tablename__ = "game_categories"

    id = db.Column(db.Integer,
                   primary_key= True)
    
    game_id = db.Column(db.Integer,
                        db.ForeignKey('games.id'))
    
    cat_id = db.Column(db.Text, 
                       db.ForeignKey('categories.id'))


class GameCollection(db.Model):
    """stores the games in a users collection"""

    __tablename__ = "game_collections"

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        primary_key=True,)

    game_id = db.Column(db.Integer,
                        db.ForeignKey('games.id'),
                        primary_key=True,)
    


class Wishlist(db.Model):
    '''stores games in a users wishlist'''

    __tablename__ = "wishes"

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        primary_key=True,)

    game_id = db.Column(db.Integer,
                        db.ForeignKey('games.id'),
                        primary_key=True,)

    subscribe_price_alerts = db.Column(db.Boolean,
                                       default=False)

    price_alert_trigger = db.Column(db.Integer)


