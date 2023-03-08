from app import *


def remove_tags(html):
    """parse html tags from the api data"""
    soup = BeautifulSoup(html, 'html.parser')
    
    for data in soup(['style','script']):
        data.decompose()

    return ''.join(soup.stripped_strings)