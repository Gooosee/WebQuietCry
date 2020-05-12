import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class LeaderBoard(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'LeaderBoard'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    record = sqlalchemy.Column(sqlalchemy.INTEGER, nullable=True)

    def __repr__(self):
        return [self.name, self.record]
