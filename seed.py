from user_models import User,db
from game_models import GameCollection, Wishlist, Category, Mechanic
from playlog_models import Playlog, PlaySession
from functions import get_categories, get_mechanics
from app import app


"""clears the database and recreates all tables"""
db.drop_all()
db.create_all()

"""populates the mechanics table with the info pulled from that api endpoint"""
get_mechanics()

"""populates the categories table with the info pulled from that api endpoint """
get_categories()