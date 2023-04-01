from game_models import Mechanic,Category
from user_models import db
import requests
import os

BASE_URL = 'https://api.boardgameatlas.com/api'
client_id = os.getenv('client_id')



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

