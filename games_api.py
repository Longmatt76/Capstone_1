from game_models import Mechanic,Category
from user_models import db
import requests
import os
from flask import flash, render_template

BASE_URL = 'https://api.boardgameatlas.com/api'
client_id = os.getenv('client_id')



def get_search(query, start):
    try:
        resp = requests.get(f'{BASE_URL}/search',
                        params={'fuzzy_match': True, 'limit': 30, 'skip': start, 'client_id': client_id, 'name': query})
        return resp.json()
    
    except: 
        flash('Sorry, an error occured when accessing the API please try again', 'danger')
        return render_template('search.html')


def get_game_data(api_id):
    resp = requests.get(f'{BASE_URL}/search',
                        params={ 'client_id': client_id, 'ids': api_id})
    return resp.json()



def get_game_value(game_id):
      resp = requests.get(f'{BASE_URL}/game/prices',
                        params={'pretty': 'true', 'game_id': game_id, 'client_id': client_id})
      return resp.json()


def get_images(api_id):
     resp = requests.get(f'{BASE_URL}/game/images',
                         params={'pretty': 'true', 'client_id': client_id, 'limit': 50, 'game_id': api_id})
     return resp.json()


def get_videos(api_id):
     resp = requests.get(f'{BASE_URL}/game/videos',
                         params={'pretty': 'true', 'client_id': client_id, 'limit': 50, 'game_id': api_id})
     return resp.json()


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

