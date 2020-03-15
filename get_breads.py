import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/List_of_breads'

def make_url(thumb_url):
    end_list = thumb_url.split('/')[6:9]
    base_url = 'https://upload.wikimedia.org/wikipedia/commons'
    for i in end_list:
        base_url += f'/{i}'
    return base_url

def get_breads():
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='mw-content-text')
    table = results.find_all('tbody')[0]
    items = table.find_all('tr')
    breads = []
    for item in items[1:]:
        columns = item.find_all('td')
        if len(columns) == 5:
            bread_title = columns[0].text.strip()
            bread_image = make_url(f"https:{columns[1].find('img')['src']}") if columns[1].find('img') else None
            bread_type = columns[2].text.strip()
            bread_origin = columns[3].text.strip()
            bread_description = columns[4].text.strip()
            if None in (bread_title, bread_image, bread_type, bread_origin, bread_description):
                continue
            text = f'{bread_title} is a type of {bread_type.lower()} from {bread_origin}. {bread_description}'
            breads.append({'text': text, 'image': bread_image})
    return breads