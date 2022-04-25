import sqlalchemy
from sqlalchemy import Column, orm

from data.db_session import SqlAlchemyBase


class Genre(SqlAlchemyBase):
    __tablename__ = "genre"
    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = Column(sqlalchemy.String, nullable=True, unique=True)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name


class Album(SqlAlchemyBase):
    __tablename__ = "album"
    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = Column(sqlalchemy.String, nullable=False)
    description = Column(sqlalchemy.String, nullable=False)
    year = Column(sqlalchemy.Integer, nullable=False)
    cover_url = Column(sqlalchemy.String, nullable=True)

    author_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"), nullable=False)
    author = orm.relation("BlacklandUser")

    genre_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("genre.id"), nullable=False)
    genre = orm.relation("Genre")

    songs = orm.relation("Song", back_populates='album')

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_year(self):
        return self.year

    def get_cover_url(self):
        return self.cover_url

    def get_author(self):
        return self.author

    def get_genre(self):
        return self.genre

    def get_songs(self):
        return self.songs

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def set_year(self, year):
        self.year = year

    def set_cover_url(self, cover_url):
        self.cover_url = cover_url
