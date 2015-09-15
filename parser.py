from bs4 import BeautifulSoup
import requests

data = requests.get('https://www.countries-ofthe-world.com/all-countries.html').text

data_li =  BeautifulSoup(data)
for ab in data_li('li'):
    print ab.text

