from bs4 import BeautifulSoup
from game_models import Mechanic,Category
from user_models import db
import requests

BASE_URL = 'https://api.boardgameatlas.com/api'
client_id = 'XlXxjnv76F'


# def remove_tags(html):
#     """parse html tags from the api data"""
#     soup = BeautifulSoup(html, 'html.parser')
    
#     for data in soup(['style','script']):
#         data.decompose()

#     return ''.join(soup.stripped_strings)



def average(lst):
    return sum(lst) / len(lst)


def get_mechanics():
    resp = requests.get(f'{BASE_URL}/game/mechanics',
                    params={'client_id': client_id})
    mechs = resp.json()
    for num in range(len(mechs['mechanics'])):
        num = Mechanic(id=mechs['mechanics'][num]['id'],name=mechs['mechanics'][num]['name'])
        db.session.add(num)

    db.session.commit()
    return


def get_categories():
    resp = requests.get(f'{BASE_URL}/game/categories',
                    params={'client_id': client_id})
    cats = resp.json()
    for num in range(len(cats['categories'])):
        num = Category(id=cats['categories'][num]['id'],name=cats['categories'][num]['name'])
        db.session.add(num)

    db.session.commit()
    return


# def get_or_create_game(id, data):
#     game = db.session.query(Game).filter_by(id=id).first()
#     if game:
#         return game
#     else:   
#         game = Game(id=id, name=data['games'][0]['name'],
#                     thumb_url=data['games'][0]['thumb_url'])
        
#         db.session.add(game)
#         db.session.commit()
#         return game