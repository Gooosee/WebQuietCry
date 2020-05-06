import flask
from flask import redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@app.route('/')
@app.route('/news')
def main():
    return flask.render_template('news.html')


@app.route('/about_us')
def about_us():
    return flask.render_template('about_us.html')


@app.route('/leaderboard')
def leaderboard():
    return flask.render_template('leaderboard.html')


@app.route('/download')
def download():
    return flask.render_template('download.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return flask.render_template('registr.html', title='Авторизация', form=form)


@app.route('/donate')
def donate():
    return flask.render_template('donate.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
