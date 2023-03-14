import requests
from game_models import Mechanic
from user_models import db

BASE_URL = 'https://api.boardgameatlas.com/api'
client_id = 'XlXxjnv76F'


# def search_API():
#     resp = requests.get(f'{BASE_URL}/images',
#                 params={'fuzzy_,match': 'true', 'limit': 15, 'client_id': client_id, 'name': 'catan'})
    

#     data = resp.json()
#     for num in range(len(data['games'])):
#         print(data['games'][num]['thumb_url'])

# skip = 0
# games = []

# while True:
#     print('-----')
#     url =       f'{BASE_URL}/search?skip={skip}&limit=30&name=Catan&pretty=true&client_id={client_id}'
#     print('Requesting', url)
#     res = requests.get(url)
#     data = res.json()
#     if data['games']== 0:
#         break
   
#     games.extend(data['games'])
#     skip = skip + 30

    





# for num in range(len(data['gameWithPrices']['used'])):
#     print(data['gameWithPrices']['used'][num]['price_text'])


# resp = requests.get(f'{BASE_URL}/search',
#                 params={'name': 'On Mars','client_id': client_id, 'limit':1, 'exact': 'true' })

# data = resp.json()

# for property in data['games']:
#     print(property)

def get_mechanics():
    resp = requests.get(f'{BASE_URL}/game/mechanics',
                    params={'client_id': client_id})
    mechs = resp.json()
    for num in range(len(mechs['mechanics'])):
        num = Mechanic(id=mechs['mechanics'][num]['id'],name=mechs['mechanics'][num]['name'])
        db.session.add(num)

    db.session.commit()
    return