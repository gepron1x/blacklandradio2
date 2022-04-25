import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import Column, orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class BlacklandUser(SqlAlchemyBase, UserMixin):
    __tablename__ = "user"

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(sqlalchemy.String, nullable=False)
    email = Column(sqlalchemy.String, unique=True, nullable=False)
    password = Column(sqlalchemy.String, nullable=False)
    description = Column(sqlalchemy.String, nullable=True)
    avatar_url = Column(sqlalchemy.String, nullable=True)
    albums = orm.relation("Album", back_populates='author')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_description(self):
        return self.description

    def get_avatar(self):
        return self.avatar_url

    def get_albums(self):
        return self.albums

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

