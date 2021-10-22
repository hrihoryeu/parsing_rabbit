import time

import requests
from bs4 import BeautifulSoup
from functions import unchaining
from math import ceil
import abc


class AbstractParser(abc.ABC):
    def __init__(self, link: str):
        self.link = link

    def pre_parsing(self):
        request = requests.get(self.link)
        soup = BeautifulSoup(request.text, 'html.parser')
        return soup

    @abc.abstractmethod
    def parsing(self) -> tuple:
        pass


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
            print(unchaining(str(soup.find('span', {'class': 'price-block__final-price'}))).replace(' ', ''))
            price = int(unchaining(str(soup.find('span', {'class': 'price-block__final-price'}))).replace(' ', '')[:-1])
            price = ceil(price * self.currency_rate * 100)
            unique_id = str(soup.find('p', {'class': 'same-part-kt__article'}))
            unique_id = unique_id[unique_id.find('1S}">') + 5:]
            unique_id = unique_id[:unique_id.find('<')]
            yield 'wb', name, price, unique_id


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
                yield 'lamoda', name, price, unique_id


class ParserRunner:
    @staticmethod
    def choose_parser(link):
        parsers_dict = {
            'www.lamoda.by': LamodaParser,
            'by.wildberries.ru': WBParser
        }
        return parsers_dict[link[8:link.find('/', 8)]](link)
