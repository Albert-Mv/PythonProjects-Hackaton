import requests
from lxml import etree
import os
import io
import shutil

def addNewsUrl(url):
    fh = os.open("url.txt", os.O_RDWR | os.O_CREAT)
    os.write(fh, str(url).encode())
    os.close(fh)

def updateNewsNumber(num):
    os.chdir('../')
    fh = os.open("0.txt", os.O_RDWR | os.O_CREAT)
    num = abs(num - 8)
    os.write(fh, str(num).encode())
    os.close(fh)
    os.chdir('News')
    
def saveNewsFiles(title, description, images_links, url):
    if(checkNews(title)):
        return
    dirs = []
    if not os.path.exists(os.getcwd()+"/News"):
        os.mkdir('News')
        os.chdir('News')
        os.mkdir("1")
        os.chdir("1")
        file = os.open("title.txt", os.O_CREAT | os.O_RDWR)
        os.write(file, str(title).replace("""['""","").replace("""']""","").encode())
        os.close(file)
        desc = os.open("description.txt", os.O_CREAT | os.O_RDWR)
        for i in range(len(description)):
            os.write(desc, str(description[i]+"\n").encode())
        os.close(desc)
        img = os.open("images.txt", os.O_CREAT | os.O_RDWR)
        for i in range(len(images_links)):
            os.write(img, str(images_links[i] + "\n").encode())
        os.close(img)
        img_count = os.open("images_count.txt", os.O_CREAT | os.O_RDWR)
        os.write(img_count, str(len(images_links)).encode())
        os.close(img_count)
        addNewsUrl(url)
        os.chdir('../../')
        return
    max = 0
    os.chdir('News')
    for dirname in os.listdir(os.getcwd()):
        if max < int(dirname):
            max = int(dirname)
    os.mkdir(str(max+1))
    updateNewsNumber(max)
    os.chdir(str(max+1))
    fh = os.open("title.txt", os.O_RDWR | os.O_CREAT)
    os.write(fh, str(title).replace("""['""","").replace("""']""","").encode())
    os.close(fh)
    desc = os.open("description.txt", os.O_CREAT | os.O_RDWR)
    for i in range(len(description)):
        os.write(desc, str(description[i]+"\n").encode())
    os.close(desc)
    img = os.open("images.txt", os.O_CREAT | os.O_RDWR)
    for i in range(len(images_links)):
        os.write(img, str(images_links[i] + "\n").encode())
    os.close(img)
    img_count = os.open("images_count.txt", os.O_CREAT | os.O_RDWR)
    os.write(img_count, str(len(images_links)).encode())
    os.close(img_count)
    addNewsUrl(url)
    os.chdir('../../')

def checkNews(title):
    dirs = []
    if not os.path.exists('News'):
        return False
    os.chdir('News')
    for dirname in os.listdir(os.getcwd()):
        dirs.append(dirname)
    os.chdir('../')
    for item in dirs:
        file = io.open(os.getcwd()+'/News/'+str(item)+'/title.txt', mode="r", encoding="utf-8")
        text = file.read()
        if(title == text):
            file.close()
            return True
        file.close()
    return False

def loadData():
    parser = MainPageParser("https://admtyumen.ru/ogv_ru/news/subj/all.htm")
    data = parser.getData()
    data.reverse()
    for i in range(len(data)):
        saveNewsFiles(data[i].title, data[i].description, data[i].images_links, data[i].url)

class NewsItem:
    def __init__(self, title, description, images_links, url):
        self.title = title
        self.description = description
        self.images_links = images_links
        self.url = url

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
        count = 10
        if(count > len(titles)):
            count = len(titles)
        for i in range(count):
            if checkNews(titles[i]):
                continue
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
        item = NewsItem(title, description, images_links, url)
        return item
