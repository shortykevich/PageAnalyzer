from bs4 import BeautifulSoup
from unicodedata import normalize


def parse_response(text):
    result = {
        'h1': '',
        'title': '',
        'description': ''
    }
    soup = BeautifulSoup(text, 'html.parser')

    h1 = soup.find('h1')
    title = soup.find('title')
    description = soup.find('meta', attrs={'name': 'description'})

    result['h1'] = normalize('NFKD', h1.get_text()) if h1 else ''
    result['title'] = normalize('NFKD', title.get_text()) if title else ''
    result['description'] = description.get('content') if description else ''
    return result
