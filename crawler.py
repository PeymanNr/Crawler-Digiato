import requests, json
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from parser import PageParser
from storage import MongoStorage, FileStorage
from config import category_name, storage_neme, LINK

class CrawlerBase(ABC):

    @property
    def storage_set(self):
        if storage_neme == 'file':
           return FileStorage()
        return MongoStorage()

    @abstractmethod
    def start(self, store):
        pass

    @abstractmethod
    def store(self, data, filename=None):
        pass

    def get_page(self, url, start=0):
        response = requests.get(url + str(start))

        return response


class LinkCrawler(CrawlerBase):

    def __init__(self, link=LINK, category=category_name):
        self.link = LINK
        self.category = category_name
        super().__init__()

    def find_links(self, html_doc):
        links = list()
        soup = BeautifulSoup(html_doc, 'html.parser')
        for li in soup.find_all('a', attrs={'class': 'rowCard__title'}):
                links.append([{"url": li.get('href'), 'flag': False}])
        return links

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
            new_links = self.find_links(response.text)
            adv_links.extend(new_links)
            if start == 2:
                crawl = False
            start += 1
        return adv_links

    def start(self, store=True):
        list_href = list()
        for cat in self.category:
            links = self.get_category_links(self.link.format(cat))
            list_href.extend(links)
            if store:
                self.store(list_href, 'data')
    def store(self, data, filename):
        self.storage_set.store(data, 'data')


class DataCrawler(CrawlerBase):
    def __init__(self):
        super().__init__()
        self.parser = PageParser()
        self.link = self.__load_link()

    def __load_link(self):
        return self.storage_set.load()

    def start(self, store=True):
        data_list = list()
        url_list = list()
        for p in self.link:
            data_list.extend(p)
            for u in data_list:
                url_list.append(u['url'])
        mylist = list(set(url_list))
        print(len(mylist))
        print(len(url_list))
        for i in mylist:
            response = requests.get(i)
            # print(response.status_code)
            data = self.parser.Parser_links(response.text)
            # print(data)

            self.store(data, data.get('writer', 'sample'))

    def store(self, data, filename):
        self.storage_set.store(data, filename)
            # print(f'DataFolder/{filename}.json')
