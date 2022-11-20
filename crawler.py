import queue

import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from parser import PageParser
from storage import MongoStorage, FileStorage
from config import category_name, storage_neme, LINK
from queue import Queue
import threading


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
            links.append(li)
        return links

    def get_category_links(self, url):
        crawl = True
        adv_links = list()
        start = 1
        while crawl:
            response = self.get_page(url, start)
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
            print(f'put link to queue')
        if store:
            self.store([{"url": li.get('href'), 'flag': False} for li in list_href])

        return list_href

    def store(self, data, *args):
        self.storage_set.store(data, 'adv_links')


class DataCrawler(CrawlerBase):
    def __init__(self):
        super().__init__()
        self.parser = PageParser()
        # self.link = self.link_queue()
        self.queue = Queue()

    def get_link(self, store=True):
        while self.queue.qsize():
            page = self.queue.get()
            response = requests.get(page['url'])
            data = self.parser.Parser_links(response.text)
            if store:
                self.storage_set.store(data, data.get('writer', 'sample'))
            if storage_neme == 'mongo':
                self.storage_set.update_flag(page)
            self.queue.task_done()
            print(f'Get Completed:{self.queue.qsize()}')

    def start(self):
        for i in self.storage_set.load():
            self.queue.put(i)

        threads_list = []
        for p in range(8):
            x = threading.Thread(target=self.get_link, args=(p, ))
            threads_list.append(x)
            x.start()
        print(f"All threads Started")
        self.queue.join()
        print("All Thread Joined")

    def store(self, data, filename):
        self.storage_set.store(data, 'adv_data')
