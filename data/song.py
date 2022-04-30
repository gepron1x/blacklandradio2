import sqlalchemy
from sqlalchemy import Column, orm
from sqlalchemy.orm import relationship

from data.db_session import SqlAlchemyBase


class Song(SqlAlchemyBase):
    __tablename__ = "song"
    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = Column(sqlalchemy.String, nullable=True)
    url = Column(sqlalchemy.String, nullable=False)
    album_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("album.id", ondelete="CASCADE"), nullable=False)
    album = relationship("Album", back_populates="songs")

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_url(self):
        return self.url

    def get_album(self):
        return self.album
