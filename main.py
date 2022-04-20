import requests
from bs4 import BeautifulSoup


def get_page():

    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
                   }
        response = requests.get('https://www.sheypoor.com/', headers=headers)
    except:
        return None
    print(response.status_code)
    return response


def find_links(html_doc):
    soup = BeautifulSoup(html_doc)
    return soup.find_all('a')


if __name__ == "__main__":
    response = get_page()
    links = find_links(response.text)
    for li in links:
        print(li.get('href'))

        
