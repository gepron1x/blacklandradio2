import sqlalchemy
from sqlalchemy import Column
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class BlacklandUser(SqlAlchemyBase):
    __tablename__ = "user"

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)
    login = Column(sqlalchemy.String, unique=True, nullable=False)
    password = Column(sqlalchemy.String, nullable=False)
    description = Column(sqlalchemy.String, nullable=True)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)
