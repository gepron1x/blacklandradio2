import os.path
import shutil

import flask
import flask_login
from flask import Flask, render_template, request, url_for
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect
from flask import abort

from api import albums
from data import db_session
from data.album import Genre, Album
from data.user import BlacklandUser
from form.album_creation_form import AlbumCreationForm
from form.albums_search import SearchForm
from form.auth import RegisterForm, LoginForm
from form.genre_form import GenreForm
from pages.album_creation_page import AlbumCreationPage
from pages.album_page import AlbumPage
from pages.profile_editor_page import ProfileEditorPage
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'cdn', 'albums')

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    os.makedirs("static/cdn/albums", exist_ok=True)
    os.makedirs("db", exist_ok=True)
    db_session.global_init("db/blacklandradio.db")

    db_sess = db_session.create_session()
    genres = ["Рок", "Хип-Хоп", "Шансон"]
    for genre in genres:
        if not db_sess.query(Genre).filter(Genre.name == genre).first():
            db_sess.add(Genre(name=genre))
    db_sess.commit()
    api.add_resource(albums.AlbumsByIdResource, '/api/v2/albums/<int:album_id>')
    api.add_resource(albums.AlbumsResource, '/api/v2/albums/')
    api.add_resource(albums.SongFileResource, '/api/v2/songs/<int:song_id>')
    api.add_resource(albums.AlbumCoverResource, '/api/v2/albums/cover/<int:album_id>')
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(BlacklandUser).get(user_id)


@app.route("/")
@app.route("/index")
def index():
    db_sess = db_session.create_session()
    return render_template("main_page.html", title="Blackland Radio", albums=db_sess.query(Album).all())


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
            avatar_url=url_for('static', filename='blacklandradio.png'),
            password=generate_password_hash(form.password.data),
            description=form.description.data
        )

        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=True)
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
    return AlbumPage(app,
                     db_sess,
                     album).response()


@app.route('/albums/create', methods=['GET', 'POST'])
def album_creation():
    form = AlbumCreationForm()
    db_sess = db_session.create_session()
    user = flask_login.current_user
    return AlbumCreationPage(
        app,
        user,
        db_sess,
        form).response()


@app.route("/albums/")
def albums_list():
    db_sess = db_session.create_session()
    albums = db_sess.query(Album).all()
    return render_template("album_list_base.html", albums=albums)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/albums/search', methods=['GET', 'POST'])
def search():
    db_sess = db_session.create_session()
    form = SearchForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        value = form.value.data
        albums = db_sess.query(Album).filter(Album.name.like(f"%{value}%")).all()
    else:
        albums = db_sess.query(Album).all()

    return render_template(
        "albums_search.html",
        albums=albums,
        form=form
    )


@app.route('/my_profile')
@login_required
def my_profile():
    return redirect(f'/profile/{current_user.id}')


@app.route("/profile/edit", methods=['POST', 'GET'])
@login_required
def edit_profile():
    db_sess = db_session.create_session()
    return ProfileEditorPage(
        app,
        db_sess,
        current_user
    ).response()


@login_required
@app.route("/albums/delete/<int:album_id>")
def delete_album(album_id):
    db_sess = db_session.create_session()
    album = db_sess.query(Album).filter(Album.id == album_id).first()
    if not album:
        return abort(404)
    if album.author != current_user:
        return abort(401)
    shutil.rmtree(f"static/cdn/albums/{album.id}")
    db_sess.delete(album)
    db_sess.commit()
    return redirect("/index")


@app.route('/profile/<int:user_id>')
def profile(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(BlacklandUser).filter(BlacklandUser.id == user_id).first()
    if user is None:
        return abort(404)
    return render_template("profile.html", user=user, albums=user.albums)


@login_required
@app.route("/create_genre", methods=['GET', 'POST'])
def create_genre():
    form = GenreForm()

    if form.validate_on_submit():
        name = form.name.data
        db_sess = db_session.create_session()
        db_sess.add(Genre(name=name))
        db_sess.commit()
        return redirect("/index")

    return render_template("genre_creation.html", title="Добавить жанр", form=form)


@app.route("/about")
def about():
    text = """BlacklandRadio - полностью бесплатный и открытый музыкальный сервис. 
    Created by @gepron1x, @stepaldo, @IDontUnderstandPycharm"""
    return render_template("about.html", about=text)


if __name__ == '__main__':
    main()
