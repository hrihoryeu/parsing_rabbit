from .wb import WBParser
from .lamoda import LamodaParser


class ParserRunner:
    @staticmethod
    def choose_parser(link):
        parsers_dict = {
            'www.lamoda.by': LamodaParser,
            'by.wildberries.ru': WBParser
        }
        return parsers_dict[link[8:link.find('/', 8)]](link)
