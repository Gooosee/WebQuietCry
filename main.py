import flask
from flask import redirect, render_template
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

from data import db_session
from data.users import User

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


class RegForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


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
    formR = RegForm()
    if formR.validate_on_submit():
        if formR.password.data == formR.password2.data:
            userNew = User()
            userNew.name = formR.login.data
            userNew.email = formR.email.data
            userNew.password = formR.password.data
            session = db_session.create_session()
            session.add(userNew)
            session.commit()
            return redirect('/')
        else:
            return render_template('registr.html',
                                   message="Повторите пароль",
                                   form=formR)
    return render_template('registr.html', title='Регистрация', form=formR)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)

    return render_template('login.html', title='Авторизация', form=form)


@app.route('/donate')
def donate():
    return flask.render_template('donate.html')


if __name__ == '__main__':
    db_session.global_init("db/comments.sqlite")
    app.run(port=8080, host='127.0.0.1')
