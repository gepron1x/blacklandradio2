import sqlalchemy
from sqlalchemy import Column, orm

from data.db_session import SqlAlchemyBase


class Genre(SqlAlchemyBase):
    __tablename__ = "genre"
    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = Column(sqlalchemy.String, nullable=True, unique=True)


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

    # songs = orm.relation("Song", back_populates='album')
