import requests
from bs4 import BeautifulSoup

def getNews():
    texts = ["https://www.bbc.com/"]
    url = "https://www.bbc.com/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    result = BeautifulSoup(response.text, "html.parser")

    headlines = result.find_all(["h1", "h2", "h3"])
    dates = result.find_all("time")

    for i, h in enumerate(headlines[:10]):
        text = h.get_text(strip=True)

        if i < len(dates):
            date = dates[i].get_text(strip=True)
        else:
            date = "Date could not be found"

        if text:
            texts.append(f"{text} | {date}")

    return texts
