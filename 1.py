from data import db_session
from data.users import User

user = User()
user.name = "Пользователь 1"
user.email = "email@email.ru"
user.password = "1232321"
session = db_session.create_session()
session.add(user)
session.commit()