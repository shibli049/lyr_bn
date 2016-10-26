from flask import Flask, render_template, url_for, redirect,request

from wikisource import poet_parser
from pymarkovchain import MarkovChain
import logging
import os
logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')

sukumar_roy_url = "https://bn.wikisource.org/wiki/%E0%A6%AC%E0%A6%BF%E0%A6%B7%E0%A6%AF%E0%A6%BC%E0%A6%B6%E0%A7%8D%E0%A6%B0%E0%A7%87%E0%A6%A3%E0%A7%80:%E0%A6%B8%E0%A7%81%E0%A6%95%E0%A7%81%E0%A6%AE%E0%A6%BE%E0%A6%B0_%E0%A6%B0%E0%A6%BE%E0%A6%AF%E0%A6%BC%E0%A7%87%E0%A6%B0_%E0%A6%9B%E0%A6%A1%E0%A6%BC%E0%A6%BE"
jibonanondo_das_url="https://bn.wikisource.org/wiki/%E0%A6%AC%E0%A6%BF%E0%A6%B7%E0%A6%AF%E0%A6%BC%E0%A6%B6%E0%A7%8D%E0%A6%B0%E0%A7%87%E0%A6%A3%E0%A7%80:%E0%A6%B8%E0%A6%BE%E0%A6%A4%E0%A6%9F%E0%A6%BF_%E0%A6%A4%E0%A6%BE%E0%A6%B0%E0%A6%BE%E0%A6%B0_%E0%A6%A4%E0%A6%BF%E0%A6%AE%E0%A6%BF%E0%A6%B0"
robi_thakur_url="https://bn.wikisource.org/wiki/%E0%A6%AC%E0%A6%BF%E0%A6%B7%E0%A6%AF%E0%A6%BC%E0%A6%B6%E0%A7%8D%E0%A6%B0%E0%A7%87%E0%A6%A3%E0%A7%80:%E0%A6%97%E0%A7%80%E0%A6%A4%E0%A6%BE%E0%A6%9E%E0%A7%8D%E0%A6%9C%E0%A6%B2%E0%A6%BF"

app = Flask(__name__)
app.debug = False
app.config.from_object(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/lyrics', methods=['POST'])
def lyrics():
    artist = request.form['artist']
    lines = int(request.form['lines'])
    size = max(int(request.form['size']), 5)

    if not artist:
        return redirect(url_for('index'))
    artist = artist.lower()

    if('sukumar roy' == artist):
        lyrics = poet_parser.getPeoms(\
            poet_parser.getHtmlFromUrl(\
                sukumar_roy_url),\
            linkSelector="div.mw-category a",\
            poemSelector = "div.poem center p",\
            size=size)
    elif('jibonanondo das' == artist):
        lyrics = poet_parser.getPeoms(\
            poet_parser.getHtmlFromUrl(\
                jibonanondo_das_url),\
            poemSelector = "div.poem p",\
            size=size)
    elif('robi thakur' == artist):
        lyrics = poet_parser.getPeoms(\
            poet_parser.getHtmlFromUrl(\
                robi_thakur_url),\
            poemSelector = "div.poem p",\
            size=size)
    else:
        lyrics=""

    result = []
    logging.info(len(lyrics))
    if(len(lyrics) > 0 and len(lyrics.strip()) > 0):
        mc = MarkovChain()
        mc.generateDatabase(lyrics,sentenceSep='[।!?\n]' )
        for line in range(0, lines):
            result.append(mc.generateString())
    else:
        result = ["No poet found!"]
    logging.info(result)
    return render_template('lyrics.html', result=result, artist=artist)

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT)


