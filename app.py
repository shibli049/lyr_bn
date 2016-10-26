from flask import Flask, render_template, url_for, redirect,request

from wikisource import sukumar_parser
from pymarkovchain import MarkovChain

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

    lyrics = sukumar_parser.getPeoms(\
        sukumar_parser.getHtmlFromUrl(\
            sukumar_parser.sukumar_roy_url),\
        size=size)

    result = []
    print(len(lyrics))
    if(len(lyrics) > 0 and len(lyrics.strip()) > 0):
        mc = MarkovChain()
        mc.generateDatabase(lyrics)
        for line in range(0, lines):
            result.append(mc.generateString())
    else:
        result = ["No poet found!"]
    print(result)
    return render_template('lyrics.html', result=result, artist=artist)

if __name__ == '__main__':
    app.run()

