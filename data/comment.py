import sqlalchemy
from sqlalchemy import Column, orm

from data.db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase):

    __tablename__ = "comment"

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    content = Column(sqlalchemy.String, nullable=False)

    album_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("album.id"), nullable=False)
    album = orm.relation("Album")

    author_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"), nullable=False)
    author = orm.relation("BlacklandUser")


