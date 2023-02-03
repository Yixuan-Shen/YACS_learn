import requests
from bs4 import BeautifulSoup

html = requests.get('http://catalog.rpi.edu/content.php?catoid=24&navoid=590')

soup = BeautifulSoup(html.text, 'html.parser')

list = soup.html.body.table.tbody.find_all('strong')

# Print all dates in Academic Calendar
for item in list:
    print(item.text)
