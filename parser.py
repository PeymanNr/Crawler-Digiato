from bs4 import BeautifulSoup


class PageParser:
    def __int__(self):
        self.soup = None

    def Parser_links(self, response_text):
        self.soup = BeautifulSoup(response_text, 'html.parser')
        data = dict(title=self.title, body=self.body, writer=self.writer, published_date=self.published)
        return data

    @property
    def title(self):
        title_tag = self.soup.find('a', attrs={'class': 'rowCard__title'})
        if title_tag:
            return title_tag.text

        @property
        def body(self):
            body_tag = self.soup.find('p', attrs={'class': 'rowCard__description'})
            if body_tag:
                return body_tag.text

            @property
            def writer(self):
                writer_tag = self.soup.find('div', attrs={'class': 'rowCard__author'})
                if writer_tag:
                    return writer_tag.text

                @property
                def published_date(self):
                    published_date_tag = self.soup.find('span', attrs={'class': 'rowCard__date'})
                    if published_date_tag:
                        return published_date_tag