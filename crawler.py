import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from config import LINK
from config import category_name


class CrawlerBase(ABC):

    @abstractmethod
    def start(self):
        pass

    # @abstractmethod
    # def store(self):
    #     pass

    def get_page(self, url, start=0):
        response = requests.get(url + str(start))

        return response


class LinkCrawler(CrawlerBase):

    def __init__(self, link=LINK, category=category_name):
        self.link = LINK
        self.category = category_name
        super().__init__()

    def parser_links(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        result_soup = soup.find_all('div', attrs={'class': 'rowCard'})
        return result_soup

    def get_category_links(self, url):
        crawl = True
        adv_links = list()
        start = 1
        while crawl:
            response = self.get_page(url, start)
            # print(response.status_code)
            if response is None:
                crawl = False
                continue
            new_links = self.parser_links(response.text)
            adv_links.extend(new_links)
            if start == 3:
                crawl = False
            start += 1
        return adv_links

    def start(self):
        for cat in self.category:
            links = self.get_category_links(self.link.format(cat))
            print(f'{cat} total {len(links)} ')


class DataCrawler(CrawlerBase):
    pass

