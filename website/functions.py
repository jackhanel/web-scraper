from bs4 import BeautifulSoup
import requests


def scrapeURL(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
    except Exception:
        pass
    return None
