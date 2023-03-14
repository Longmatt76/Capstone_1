"""sqlalchemy game models for the Boardgame Shelf"""

from flask_sqlalchemy import SQLAlchemy
from user_models import db



# class Game(db.Model):
#     """stores detailed game data in the db"""

#     __tablename__ = 'games'

#     id = db.Column(db.Text,
#                    primary_key=True,)



#     def __repr__(self):
#         return f"<Game #{self.id}: {self.api_handle}, {self.name}>"


class Mechanic(db.Model):
    """stores the api data for a games mechanics"""

    __tablename__ = "mechanics"

    id = db.Column(db.TEXT,
                   primary_key=True)

    name = db.Column(db.Text,
                     nullable=False)

    


# class GameMechanic(db.Model):
#     """many to many relationship between a game and it's mechanics"""

#     __tablename__ = "game_mechanics"

#     id = db.Column(db.Integer,
#                    primary_key=True)
    
#     game_id = db.Column(db.Text,
#                    db.ForeignKey('games.id'))
    
#     mech_id = db.Column(db.Text,
#                     db.ForeignKey('mechanics.id'))


class Category(db.Model):
    """stores the api data for a games categories"""

    __tablename__ = "categories"

    id = db.Column(db.Text,
                   primary_key=True)

    name = db.Column(db.Text,
                     nullable=False)

  



# class GameCategory(db.Model):
#     """Many to many relationship between a game and it's mechanics"""

#     __tablename__ = "game_categories"

#     id = db.Column(db.Integer,
#                    primary_key= True)
    
#     game_id = db.Column(db.Text,
#                         db.ForeignKey('games.id'))
    
#     cat_id = db.Column(db.Text, 
#                        db.ForeignKey('categories.id'))


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

    used_value = db.Column(db.Text,
                           default= 'get value')
    
    

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


