from repository import SQLAlchemyRepository

from user.models import UserModel


class UserRepository(SQLAlchemyRepository):
    model = UserModel
