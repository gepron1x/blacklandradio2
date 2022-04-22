import sqlalchemy
from sqlalchemy import Column, orm

from data.db_session import SqlAlchemyBase


class Song(SqlAlchemyBase):
    __tablename__ = "song"
    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    url = Column(sqlalchemy.String, nullable=False)
    album_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("album.id"), nullable=False)
    album = orm.relation("Album")
