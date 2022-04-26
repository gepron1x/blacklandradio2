import os.path

import flask_login
from flask import Flask, render_template, request, url_for
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from data import db_session
from data.album import Genre, Album
from data.user import BlacklandUser
from form.album_creation import AlbumCreationForm
from form.auth import RegisterForm, LoginForm
from pages.album_creation_page import AlbumCreationPage
from pages.album_page import AlbumPage

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'cdn', 'albums')

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/blacklandradio.db")
    db_sess = db_session.create_session()
    genres = ["Рок", "Хип-Хоп", "Шансон"]
    for genre in genres:
        if not db_sess.query(Genre).filter(Genre.name == genre).first():
            db_sess.add(Genre(name=genre))
    db_sess.commit()
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(BlacklandUser).get(user_id)


@app.route("/")
@app.route("/index")
def index():
    return render_template("main_page.html", title="Blackland Radio")


@app.route("/register", methods=['GET', 'POST'])
def register():
    from data.user import BlacklandUser
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(BlacklandUser).filter(BlacklandUser.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = BlacklandUser(
            email=form.email.data,
            name=form.name.data,
            password=generate_password_hash(form.password.data),
            description=form.description.data
        )

        db_sess.add(user)
        db_sess.commit()
        return redirect('/index')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(BlacklandUser).filter(BlacklandUser.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/index")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/albums/<int:album_id>", methods=['GET', 'POST'])
def get_album(album_id):
    db_sess = db_session.create_session()
    album = db_sess.query(Album).filter(Album.id == album_id).first()
    return AlbumPage(app, db_sess, album).response()


@app.route('/albums/create', methods=['GET', 'POST'])
def album_creation():
    form = AlbumCreationForm()
    db_sess = db_session.create_session()
    user = flask_login.current_user
    return AlbumCreationPage(app, user, db_sess, form).response()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/my_profile')
@login_required
def my_profile():
    img_path = url_for("static", filename="blacklandradio.png")
    return render_template('my_profile.html', title='Мой профиль', path=img_path)


if __name__ == '__main__':
    main()
