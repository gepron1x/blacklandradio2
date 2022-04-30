import os

from flask import request, url_for, render_template
from sqlalchemy.orm import Session
from werkzeug.utils import redirect

from data.album import Genre, Album
from data.song import Song
from pages.page import Page


class AlbumCreationPage(Page):

    def __init__(self, app, user, db_session: Session, form):
        self.app = app
        self.user = user
        self.db_session = db_session
        self.form = form

    def save_cover(self, album):
        print(self.form.cover.data)
        cover_file_name = f"cover{os.path.splitext(self.form.cover.data.filename)[1]}"
        cover_url = os.path.join(self.app.config['UPLOAD_FOLDER'], str(album.id), cover_file_name)
        self.form.cover.data.save(cover_url)
        album.cover_url = url_for('static', filename=f"/cdn/albums/{album.id}/{cover_file_name}")

    def save_songs(self, album):

        for song_file in self.form.songs.data:
            song_url = os.path.join(self.app.config['UPLOAD_FOLDER'], str(album.id), song_file.filename)
            name = os.path.splitext(song_file.filename)[0]
            song_file.save(song_url)
            song = Song(name=name,
                        url=url_for('static', filename=f"/cdn/albums/{album.id}/{song_file.filename}"),
                        album_id=album.id)

            self.db_session.add(song)

    def response(self):
        self.form.genre.choices = list(
            map(lambda g: g.name, self.db_session.query(Genre).all())
        )
        if self.form.validate_on_submit():
            album = Album(
                name=self.form.name.data,
                description=self.form.description.data,
                year=self.form.year.data,
                author_id=self.user.id,
                genre_id=self.db_session.query(Genre).filter(Genre.name == self.form.genre.data).first().id
            )
            self.db_session.add(album)
            self.db_session.flush()

            os.mkdir(os.path.join(self.app.config['UPLOAD_FOLDER'], str(album.id)))
            self.save_cover(album)
            self.save_songs(album)
            self.db_session.commit()
            return redirect(f"/albums/{album.id}")

        return render_template('album_creation.html', title="Создание альбома", form=self.form)
