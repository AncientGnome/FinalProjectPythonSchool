import requests
from bs4 import BeautifulSoup
texts = []

def getNews():

    url = "https://www.bbc.com/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    result = BeautifulSoup(response.text, "html.parser")
    headlines = result.find_all(["h1", "h2", "h3"])

    for h in headlines[:10]:
        text = h.get_text(strip=True)
        if text:
            texts.append(text)
    return texts
getNews()
