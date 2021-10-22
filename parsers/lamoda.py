from math import ceil
from bs4 import BeautifulSoup
import requests

from .abstract import AbstractParser
from functions import unchaining


class LamodaParser(AbstractParser):
    def __init__(self, link: str):
        super().__init__(link)

    def get_amount_of_pages(self):
        """
        getting amount of pages on lamoda.by
        """
        soup = self.pre_parsing()
        amount = soup.find('span', {'class': 'products-catalog__head-counter'})
        amount = int(unchaining(str(amount)).split()[0])
        return ceil(amount / 60)

    def parsing(self):
        """
        lamoda parser
        """
        pages = self.get_amount_of_pages()

        for page in range(1, pages + 1):
            link = self.link[:-1]
            request = requests.get('{}{}'.format(link, page))
            soup = BeautifulSoup(request.text, 'html.parser')
            shoes = soup.find_all('div', {'class': 'products-list-item'})

            for shoe in shoes:
                name = unchaining(str(shoe.find('span', {'class': 'products-list-item__type'})))
                unique_id = str(shoe.find('div', {'class': 'products-list-item__extra-info'}))
                id_ = unique_id.find('data-sku')
                unique_id = unique_id[id_ + 10: unique_id.find('"', id_ + 10)]
                try:
                    price = int(float(unchaining(str(shoe.find('span', {'class': 'price__actual'})))) * 100)
                except ValueError:
                    price = int(float(unchaining(str(shoe.find('span', {'class': 'price__action'})))) * 100)
                yield unique_id, name, price, 'lamoda',
