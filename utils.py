import requests
from bs4 import BeautifulSoup as bs

def get_soup(url):
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    return soup