from flask import Flask, render_template
from flask_login import current_user
from sqlalchemy.orm import Session

from data.album import Album
from data.comment import Comment
from form.comment_form import CommentForm
from pages.page import Page


class AlbumPage(Page):

    def __init__(self, app: Flask, db_session: Session, album: Album):
        self.app = app
        self.db_session = db_session
        self.album = album

    def response(self):
        form = CommentForm()
        if form.validate_on_submit():
            comment = Comment(
                content=form.content.data,
                album_id=self.album.id,
                author_id=current_user.id
            )
            self.db_session.add(comment)
            return render_template("album_page.html", title="Альбом", album=self.album, comment_form=form)

        return render_template("album_page.html", title="Альбом", album=self.album, comment_form=form)
