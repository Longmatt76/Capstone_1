import requests

BASE_URL = 'https://api.boardgameatlas.com/api'
client_id = 'XlXxjnv76F'


# def search_API():
#     resp = requests.get(f'{BASE_URL}/images',
#                 params={'fuzzy_,match': 'true', 'limit': 15, 'client_id': client_id, 'name': 'catan'})
    

#     data = resp.json()
#     for num in range(len(data['games'])):
#         print(data['games'][num]['thumb_url'])

skip = 0
games = []

while True:
    print('-----')
    url =       f'{BASE_URL}/search?skip={skip}&limit=30&name=Catan&pretty=true&client_id={client_id}'
    print('Requesting', url)
    res = requests.get(url)
    data = res.json()
    if data['games']== 0:
        break
   
    games.extend(data['games'])
    skip = skip + 30

    





# for num in range(len(data['gameWithPrices']['used'])):
#     print(data['gameWithPrices']['used'][num]['price_text'])


# resp = requests.get(f'{BASE_URL}/search',
#                 params={'name': 'On Mars','client_id': client_id, 'limit':1, 'exact': 'true' })

# data = resp.json()

# for property in data['games']:
#     print(property)
