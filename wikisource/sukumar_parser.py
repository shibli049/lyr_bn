import requests
from bs4 import BeautifulSoup as bs

bn_wikisource_baseurl = "https://bn.wikisource.org/wiki/"
sukumar_roy_url = "https://goo.gl/Lcv5Vr"


def getHtmlFromUrl(path = None):
    response = requests.get(sukumar_roy_url, allow_redirects=True)
    # print(response)
    html = response.text
    if(path != None):
        writeToFile(path, html)
    return html

def getPeoms(html):
    """
        get the poems url from
    """
    # print(html)
    soup = bs(html, "html.parser")
    links = soup.select("div.mw-category-group a")
    for a in links:
        print(a['href'])



def writeToFile(path, content, mode = 'w'):
    with open(path, 'w') as f:
        f.write(content)

def readFile(path):
    with open(path, 'r') as f:
        data = f.read()

    return data

if __name__ == '__main__':
    from os.path import expanduser
    home = expanduser("~")
    path = home + "/Desktop/test.html"
    # writeToFile(path, "hello world!\n"*100, mode = 'a')
    # print(readFile(path))
    getPeoms(readFile(path))