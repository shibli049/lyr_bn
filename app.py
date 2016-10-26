from flask import Flask, render_template, url_for, redirect,request

from wikisource import poet_parser
from pymarkovchain import MarkovChain
import logging
logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')

sukumar_roy_url = "https://goo.gl/Lcv5Vr"
jibonanondo_das_url="https://goo.gl/0YYcuI"
robi_thakur_url="https://goo.gl/vzuTbf"

app = Flask(__name__)
app.debug = True

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
    app.run()

