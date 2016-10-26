import requests
from bs4 import BeautifulSoup as bs
import random
import logging
logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')



bn_wikisource_baseurl = "https://bn.wikisource.org"



from os.path import expanduser
home = expanduser("~")
path = home + "/test.html"


def getHtmlFromUrl(url,path = None):
    response = requests.get(url, allow_redirects=True)
    logging.debug(response)
    html = response.text
    if(path != None):
        writeToFile(path, html)
    return html

def extractPoemFromHtml(html , poemSelector = "div.poem p"):
    logging.debug(html)
    soup = bs(html, "html.parser")
    poem = soup.select(poemSelector)
    logging.debug("poem len: " + str(len(poem)))

    # writeToFile(path + "poem.txt", poem[0].text)
    logging.debug("poem start")
    logging.debug(poem)
    logging.debug(len(poem))
    logging.debug("poem end")
    if(poem != None and len(poem) > 0):
        logging.debug(poem[0].contents)
        return poem[0].text
    else:
        return ""


def getPeoms(html, linkSelector="div.mw-category a",poemSelector = "div.poem p", size = 5):
    """
        get the poems url from
    """
    logging.debug(html)
    soup = bs(html, "html.parser")
    links = soup.select(linkSelector)
    random.shuffle(links)
    choosen = []
    for link in links:
        link = bn_wikisource_baseurl + link['href']
        if("action=edit" not in link):
            choosen.append( link )
        if(len(choosen) >= size):
            break


    text = ""
    for link in choosen:
        current = extractPoemFromHtml(getHtmlFromUrl(link), poemSelector=poemSelector)
        logging.debug(current)
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
    logging.debug(readFile(path))
    lyrics = getPeoms(\
        getHtmlFromUrl(\
            sukumar_roy_url\
            ))
    print(lyrics)