from flask import Flask, render_template
from sqlalchemy.orm import Session

from data.album import Album
from pages.page import Page


class AlbumPage(Page):

    def __init__(self, app: Flask, db_session: Session, album: Album):
        self.app = app
        self.db_session = db_session
        self.album = album

    def response(self):
        return render_template("album_page.html", title="Альбом", album=self.album)
