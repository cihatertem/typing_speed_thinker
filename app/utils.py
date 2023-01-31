from bs4 import BeautifulSoup
import requests
import json

URL = "https://www.ef.com/wwen/english-resources/english-vocabulary/" \
      "top-3000-words/"


def fill_word_list() -> None:
    """
    Scraps words from the URL and saves the list as json file in the root DIR.
    :return:
    """
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    words_p = soup.select_one(
        ".field-item.even > p"
    ).get_text(
        separator=",",
        strip=True
    ).lower().split(",")

    with open("data/word_list.json", "w") as file:
        file.write(json.dumps(words_p))
