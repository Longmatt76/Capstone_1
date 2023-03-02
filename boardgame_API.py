import requests

BASE_URL = 'https://api.boardgameatlas.com/api'
client_id = 'XlXxjnv76F'
CoB_id = 'VNBC6yq1WO'
Cave_id = '0DAMHQym7H'
Agricola = '0DAMHQym7H'

resp = requests.get(f'{BASE_URL}/search',
                params={'name': 'Tzolkin', 'limit': 1, 'client_id': client_id})

data = resp.json()

print(data)

# for num in range(len(data['gameWithPrices']['used'])):
#     print(data['gameWithPrices']['used'][num]['price_text'])


# resp = requests.get(f'{BASE_URL}/search',
#                 params={'name': 'On Mars','client_id': client_id, 'limit':1, 'exact': 'true' })

# data = resp.json()

# for property in data['games']:
#     print(property)
