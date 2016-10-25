import requests
from bs4 import BeautifulSoup as bs
import random

bn_wikisource_baseurl = "https://bn.wikisource.org"
sukumar_roy_url = "https://goo.gl/Lcv5Vr"


from os.path import expanduser
home = expanduser("~")
path = home + "/Desktop/test.html"


def getHtmlFromUrl(url,path = None):
    response = requests.get(url, allow_redirects=True)
    # print(response)
    html = response.text
    if(path != None):
        writeToFile(path, html)
    return html

def extractPoemFromHtml(html):
    soup = bs(html, "html.parser")
    poem = soup.select("div.poem>center p")
    writeToFile(path + "poem.txt", poem)


def getPeoms(html, size = 5):
    """
        get the poems url from
    """
    # print(html)
    soup = bs(html, "html.parser")
    links = soup.select("div.mw-category-group a")
    choosen = []
    for i in range(size):
        choosen.append( bn_wikisource_baseurl + random.choice(links)['href'])


    for link in choosen:
        print( extractPoemFromHtml(getHtmlFromUrl(link)) )
        break

    print(len(choosen))

def writeToFile(path, content, mode = 'w'):
    with open(path, 'w') as f:
        f.write(content)

def readFile(path):
    with open(path, 'r') as f:
        data = f.read()

    return data

if __name__ == '__main__':

    # writeToFile(path, "hello world!\n"*100, mode = 'a')
    # print(readFile(path))
    getPeoms(readFile(path), 10)