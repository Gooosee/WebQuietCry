import flask

app = flask.Flask(__name__)


@app.route('/')
@app.route('/news')
def main():
    return flask.render_template('WebQuietCry.html')


@app.route('/about_us')
def about_us():
    return flask.render_template('WebQuietCry.html')


@app.route('/leaderboard')
def leaderboard():
    return flask.render_template('WebQuietCry.html')


@app.route('/download')
def download():
    return flask.render_template('WebQuietCry.html')


@app.route('/donate')
def donate():
    return flask.render_template('WebQuietCry.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
