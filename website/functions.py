from bs4 import BeautifulSoup
import requests


def scrapeURL(url):
    response = requests.get(url)
    if response.status_code != 200:
        return response.status_code
    
    soup = BeautifulSoup(response.text, "html.parser")
    return soup