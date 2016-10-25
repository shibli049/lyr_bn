from flask import Flask, render_template, url_for, redirect,request


app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/lyrics', methods=['POST'])
def lyrics():
    artist = request.form['artist']
    lines = int(request.form['lines'])

    if not artist:
        return redirect(url_for('index'))

    return render_template('lyrics.html', result=['hello', 'world'], artist=artist)

if __name__ == '__main__':
    app.run()

