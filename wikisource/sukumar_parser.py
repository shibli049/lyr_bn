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
    # print(html)
    soup = bs(html, "html.parser")
    poem = soup.select("div.poem center p")
    # print("poem len: " + str(len(poem)))
    # print(poem[0].contents)
    # writeToFile(path + "poem.txt", poem[0].text)
    # print("poem start")
    # print(poem)
    # print(len(poem))
    # print("poem end")
    if(poem != None and len(poem) > 0):
        return poem[0].text
    else:
        return ""


def getPeoms(html, size = 5):
    """
        get the poems url from
    """
    print(html)
    soup = bs(html, "html.parser")
    links = soup.select("div.mw-category-group a")
    choosen = []
    for i in range(size):
        link = bn_wikisource_baseurl + random.choice(links)['href']
        print(link)
        choosen.append( link )


    text = ""
    for link in choosen:
        current = extractPoemFromHtml(getHtmlFromUrl(link))
        print(current)
        text += current
        if(len(text) > 0 and not text.endswith("\n")):
            text += "\n"

    return text




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
    lyrics = getPeoms(\
        getHtmlFromUrl(\
            sukumar_roy_url\
            ))
    print(lyrics)