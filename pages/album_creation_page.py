import os

from flask import request, url_for, render_template
from werkzeug.utils import redirect

from data.album import Genre, Album
from data.song import Song
from pages.page import Page


class AlbumCreationPage(Page):

    def __init__(self, app, user, db_session, form):
        self.app = app
        self.user = user
        self.db_session = db_session
        self.form = form

    def save_cover(self, album):
        cover_file_name = f"cover{os.path.splitext(self.form.cover.data)[1]}"
        print(cover_file_name)
        cover_url = os.path.join(self.app.config['UPLOAD_FOLDER'], str(album.id), cover_file_name)
        print(cover_file_name)
        print(request.files)
        request.files["cover"].save(cover_url)
        album.cover_url = cover_url

    def save_songs(self, album):
        print(self.form.songs.data)
        for song_file in self.form.songs.data:
            print("hey")
            song_url = os.path.join(self.app.config['UPLOAD_FOLDER'], str(album.id), song_file)
            request.files[song_file].save(song_url)
            song = Song(url=song_url, album_id=album.id)
            self.db_session.add(song)

    def response(self):
        self.form.genre.choices = list(
            map(lambda g: g.name, self.db_session.query(Genre).all())
        )
        if self.form.validate_on_submit():
            print("works")
            album = Album(
                name=self.form.name.data,
                description=self.form.description.data,
                year=self.form.year.data,
                author_id=self.user.id,
                genre_id=self.db_session.query(Genre).filter(Genre.name == self.form.genre.data).first().id
            )
            self.db_session.add(album)
            self.db_session.flush()

            print("????")
            self.save_cover(album)
            print("????")
            self.save_songs(album)
            print("????")
            self.db_session.commit()
            return redirect("/index")

        return render_template('album_creation.html', title="Создание альбома", form=self.form)
