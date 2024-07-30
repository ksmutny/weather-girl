import requests
from bs4 import BeautifulSoup

def fetch_html_content(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    
    return response.text

def data_cell(n):
    selector = f'#data-koupaliste .row .row > div:nth-child({n}) div.media-body h1'
    elements = soup.select(selector)

    return elements[0].get_text(strip=True)


html = fetch_html_content('https://koupalistepetynka.cz/')
soup = BeautifulSoup(html, 'html.parser')

water_temp = data_cell(1)
air_temp = data_cell(2)
visitor_count = data_cell(3)

print(f'Water temperature: {water_temp}')
print(f'Air temperature: {air_temp}')
print(f'Visitor count: {visitor_count}')
