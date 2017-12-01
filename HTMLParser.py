import requests
from lxml import etree

def start():
    parser = MainPageParser("https://admtyumen.ru/ogv_ru/news/subj/all.htm")
    for i in range(len(parser.getData())):
        print(parser.getData()[i].title)
        print(parser.getData()[i].description)
        print(parser.getData()[i].images_links)

class NewsItem:
    def __init__(self, title, description, images_links):
        self.title = title
        self.description = description
        self.images_links = images_links

class MainPageParser:
    _news = []
    def __init__(self, url):
        self.url = url
        self.initialization()

    def initialization(self):
        page = requests.get(self.url)
        tree = etree.HTML(page.text)
        titles = tree.xpath('//a[@class="summary"]/text()')
        descriptions = tree.xpath('//div[@class="resume"]/text()')
        images_links = tree.xpath('//a[@class="pct"]/img/@src')
        full_news_links = tree.xpath('//a[@class="summary"]/@href')
        news_page_parser = NewsPageParser()
        for i in range(len(titles)):
            item = news_page_parser.getNewsItem("https://admtyumen.ru/"+full_news_links[i])
            if not item.images_links:
                item.images_links = images_links
            self._news.append(item)

    def getData(self):
        return self._news

class NewsPageParser:
    def getNewsItem(self, url):
        page = requests.get(url)
        tree = etree.HTML(page.text)
        title = tree.xpath('//h1/text()')
        description = tree.xpath('//div[@id="divZoneCenter"]/p/text()')
        images_links = tree.xpath('//div[@id="divZoneCenter"]/img/@src')
        title = str(title).replace('\\xa0', ' ')
        for i in range(len(description)):
            description[i] = str(description[i]).replace('\\xa0', ' ')
        item = NewsItem(title, description, images_links)
        return item

start()