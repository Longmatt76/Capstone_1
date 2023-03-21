"""sqlalchemy game models for the Boardgame Shelf"""

from flask_sqlalchemy import SQLAlchemy
from user_models import db




class Mechanic(db.Model):
    """stores the api data for a games mechanics so it can be crossreferenced to retrieve a games 
       mechanics without having to send an additional request to the API"""

    __tablename__ = "mechanics"

    id = db.Column(db.TEXT,
                   primary_key=True)

    name = db.Column(db.Text,
                     nullable=False)

    


class Category(db.Model):
    """stores the api data for a games categories so it can be crossreferenced to retrieve a games 
       categories without having to send an additional request to the API"""

    __tablename__ = "categories"

    id = db.Column(db.Text,
                   primary_key=True)

    name = db.Column(db.Text,
                     nullable=False)

  


class GameCollection(db.Model):
    """stores the games in a users collection"""

    __tablename__ = "game_collections"


    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='CASCADE'),
                        primary_key=True,)

    game_id = db.Column(db.Text,
                        primary_key=True,)
    
    
    name = db.Column(db.Text,
                     nullable=False,)

    thumb_url = db.Column(db.Text)
    
    comments = db.Column(db.String(90),
                         default="add comment")

    rating = db.Column(db.Text, 
                       default= 'add rating')

    used_value = db.Column(db.Float)
    
    

class Wishlist(db.Model):
    '''stores games in a users wishlist'''

    __tablename__ = "wishes"

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='CASCADE'),
                        primary_key=True,)

    game_id = db.Column(db.Text,
                        primary_key=True,)
    
    name = db.Column(db.Text,
                     nullable=False,)

    thumb_url = db.Column(db.Text)

    subscribe_price_alerts = db.Column(db.Boolean,
                                       default=False)

    price_alert_trigger = db.Column(db.Integer)


