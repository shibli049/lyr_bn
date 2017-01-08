import requests
from bs4 import BeautifulSoup as bs
import random
import logging
import zipfile
logging.basicConfig(level=logging.INFO,
                    format=' %(asctime)s - %(levelname)s - %(message)s')


bn_wikisource_baseurl = "https://bn.wikisource.org"
from os.path import expanduser
home = expanduser("~")
path = home + "/test.html"


def getHtmlFromUrl(url, path=None):
    response = requests.get(url, allow_redirects=True)
    logging.debug(response)
    html = response.text
    if(path != None):
        writeToFile(path, html)
    return html


def extractPoemFromHtml(html, poemSelector="div.poem p"):
    logging.debug(html)
    soup = bs(html, "html.parser")
    peomsParas = soup.select(poemSelector)
    logging.debug("poem len: " + str(len(peomsParas)))

    # writeToFile(path + "poem.txt", poem[0].text)
    logging.debug("poem start")
    # logging.debug(poem)
    logging.debug(len(peomsParas))
    logging.debug("poem end")
    if(peomsParas != None and len(peomsParas) > 0):
        text = ""
        for peomsPara in peomsParas:
            text += peomsPara.text + "\n"
        return text.strip() + "\n"
    else:
        return ""


def getPeoms(html, linkSelector="div.mw-category a", poemSelector="div.poem p", size=5):
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
            choosen.append(link)
        # if(len(choosen) >= size):
        #     break

    text = ""
    for link in choosen:
        current = extractPoemFromHtml(
            getHtmlFromUrl(link), poemSelector=poemSelector)
        logging.debug(current)
        text += current
        if(len(text) > 0 and not text.endswith("\n")):
            text += "\n"

    return text.strip() + "\n"


def writeToFile(path, content, mode='w'):
    with open(path, 'w') as f:
        f.write(content)


def readFile(path):
    data = ""
    try:
        with open(path, 'r') as f:
            data = f.read()
    except FileNotFoundError as err:
        pass

    return data

if __name__ == '__main__':

    jibonanondo_das_url = "https://bn.wikisource.org/wiki/%E0%A6%AC%E0%A6%BF%E0%A6%B7%E0%A6%AF%E0%A6%BC%E0%A6%B6%E0%A7%8D%E0%A6%B0%E0%A7%87%E0%A6%A3%E0%A7%80:%E0%A6%B8%E0%A6%BE%E0%A6%A4%E0%A6%9F%E0%A6%BF_%E0%A6%A4%E0%A6%BE%E0%A6%B0%E0%A6%BE%E0%A6%B0_%E0%A6%A4%E0%A6%BF%E0%A6%AE%E0%A6%BF%E0%A6%B0"
    robi_thakur_url = "https://bn.wikisource.org/wiki/%E0%A6%AC%E0%A6%BF%E0%A6%B7%E0%A6%AF%E0%A6%BC%E0%A6%B6%E0%A7%8D%E0%A6%B0%E0%A7%87%E0%A6%A3%E0%A7%80:%E0%A6%97%E0%A7%80%E0%A6%A4%E0%A6%BE%E0%A6%9E%E0%A7%8D%E0%A6%9C%E0%A6%B2%E0%A6%BF"

    sukumar_roy_url = "https://bn.wikisource.org/wiki/%E0%A6%AC%E0%A6%BF%E0%A6%B7%E0%A6%AF%E0%A6%BC%E0%A6%B6%E0%A7%8D%E0%A6%B0%E0%A7%87%E0%A6%A3%E0%A7%80:%E0%A6%B8%E0%A7%81%E0%A6%95%E0%A7%81%E0%A6%AE%E0%A6%BE%E0%A6%B0_%E0%A6%B0%E0%A6%BE%E0%A6%AF%E0%A6%BC%E0%A7%87%E0%A6%B0_%E0%A6%9B%E0%A6%A1%E0%A6%BC%E0%A6%BE"
    logging.debug(readFile(path))
    lyrics = getPeoms(
        getHtmlFromUrl(
            jibonanondo_das_url
        ))
    if(len(lyrics) > 0):
        writeToFile(home + "/jibonanondo_das.txt", lyrics)
        # from zipfile_infolist import print_info
        # import zipfile
        # zf = zipfile.ZipFile(home + '/poets.zip', mode='w')
        # try:
        #     import zlib
        #     compression = zipfile.ZIP_DEFLATED
        # except:
        #     compression = zipfile.ZIP_STORED

        # modes = { zipfile.ZIP_DEFLATED: 'deflated',
        # zipfile.ZIP_STORED:   'stored',
        # }
        # try:
        #     zf.writestr('sukumar.txt', lyrics)
        # finally:
        #     zf.close()
    # print(lyrics)
