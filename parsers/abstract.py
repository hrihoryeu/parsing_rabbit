import requests
import abc
from bs4 import BeautifulSoup


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
