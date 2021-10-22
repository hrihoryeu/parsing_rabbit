from .abstract import AbstractParser
from bs4 import BeautifulSoup
import requests
from functions import unchaining
from math import ceil


class WBParser(AbstractParser):
    def __init__(self, link: str):
        super().__init__(link)
        self.currency_rate = float(input(' [x] Enter current BYN - RUB currency rate: '))

    def parsing(self) -> tuple:
        """
        wildberries parser
        """
        soup = self.pre_parsing()
        cards = soup.find_all('a', {'class': 'product-card__main'})
        for card in cards:
            link = 'https://by.wildberries.ru' + card.get('href')
            response = requests.get(link)
            if response.status_code != 200:
                continue
            soup = BeautifulSoup(response.text, 'html.parser')
            name = str(soup.find('h1', {'class': 'same-part-kt__header'}))[142:]
            name = name[:name.find('<')]
            price = int(unchaining(str(soup.find('span', {'class': 'price-block__final-price'}))).replace(' ', '')[:-1])
            price = ceil(price * self.currency_rate * 100)
            unique_id = str(soup.find('p', {'class': 'same-part-kt__article'}))
            unique_id = unique_id[unique_id.find('1S}">') + 5:]
            unique_id = unique_id[:unique_id.find('<')]
            yield unique_id, name, price, 'wb'
