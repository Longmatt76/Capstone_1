from bs4 import BeautifulSoup
from app import db

# def remove_tags(html):
#     """parse html tags from the api data"""
#     soup = BeautifulSoup(html, 'html.parser')
    
#     for data in soup(['style','script']):
#         data.decompose()

#     return ''.join(soup.stripped_strings)



def average(lst):
    return sum(lst) / len(lst)


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