import flask
from flask import redirect, render_template, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

from data import db_session
from data.comments import Comments
from data.leaderBoard import LeaderBoard
from data.news import News
from data.users import User

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    submit = SubmitField('Добавить')


class ComForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    submit = SubmitField('Добавить')


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


class addRecordForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    submit = SubmitField('Добавить')


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
    session = db_session.create_session()
    news = session.query(News)
    return render_template("news.html", news=news)


@app.route('/about_us')
def about_us():
    return flask.render_template('about_us.html')


@app.route('/leaderboard')
def leaderboard():
    return flask.render_template('leaderboard.html')


@app.route('/download')
def download():
    session = db_session.create_session()
    comments = session.query(Comments)
    return render_template("download.html", comments=comments)


@app.route('/reg', methods=['GET', 'POST'])
def reqister():
    form = RegForm()
    if form.validate_on_submit():
        if form.password.data != form.password2.data:
            return render_template('registr.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('registr.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.name = form.login.data
        user.email = form.email.data
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('registr.html', title='Регистрация', form=form)


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


@app.route('/addNews',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        current_user.news.append(news)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('addNews.html', title='Добавление новости',
                           form=form)


@app.route('/addCom', methods=['GET', 'POST'])
@login_required
def add_com():
    form = ComForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        com = Comments()
        com.title = form.title.data
        com.content = form.content.data
        current_user.com.append(com)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('addCom.html', title='Добавление комментария',
                           form=form)


@app.route('/addCom/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_com(id):
    form = ComForm()
    if request.method == "GET":
        session = db_session.create_session()
        com = session.query(Comments).filter(Comments.id == id,
                                          Comments.user == current_user).first()
        if com:
            form.title.data = com.title
            form.content.data = com.content
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        com = session.query(Comments).filter(Comments.id == id,
                                          Comments.user == current_user).first()
        if com:
            com.title = form.title.data
            com.content = form.content.data
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('addCom.html', title='Редактирование комментария', form=form)


@app.route('/com_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def com_delete(id):
    session = db_session.create_session()
    com = session.query(Comments).filter(Comments.id == id,
                                      Comments.user == current_user).first()
    if com:
        session.delete(com)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/addNews/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        session = db_session.create_session()
        news = session.query(News).filter(News.id == id,
                                          News.user == current_user).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        news = session.query(News).filter(News.id == id,
                                          News.user == current_user).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('addNews.html', title='Редактирование новости', form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    session = db_session.create_session()
    news = session.query(News).filter(News.id == id,
                                      News.user == current_user).first()
    if news:
        session.delete(news)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/donate')
def donate():
    return flask.render_template('donate.html')


@app.route('/addRecord/<int:score>', methods=['GET', 'POST'])
def addRecord(score):
    form = addRecordForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        LB = LeaderBoard()
        LB.name = form.login.data
        LB.record = int(score)
        session.add(LB)
        session.commit()
        return redirect('/')
    return render_template('addRecord.html', title='Добавление новости',
                           form=form)


if __name__ == '__main__':
    db_session.global_init("db/comments.sqlite")
    app.run(port=8080, host='127.0.0.1')
