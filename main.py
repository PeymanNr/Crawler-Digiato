import sys
from crawler import LinkCrawler, DataCrawler

if __name__ == '__main__':
    switch = sys.argv[1]
    if switch == 'find_link':
        p = LinkCrawler()
        p.start()
    elif switch == 'save_data':
        p = DataCrawler()
        p.start()
