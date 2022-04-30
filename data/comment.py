import sqlalchemy
from sqlalchemy import Column, orm
from sqlalchemy.orm import relationship

from data.db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase):

    __tablename__ = "comment"

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    content = Column(sqlalchemy.String, nullable=False)

    album_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("album.id", ondelete="CASCADE"), nullable=False)
    album = relationship("Album", back_populates="comments")

    author_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    author = orm.relation("BlacklandUser")

    def get_id(self):
        return self.id

    def get_content(self):
        return self.content

    def get_album(self):
        return self.album

    def get_author(self):
        return self.author

