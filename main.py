import flask

app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.render_template('WebQuietCry.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
