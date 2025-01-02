from repository import SQLAlchemyRepository

from user.models import UserBuildingModel, UserModel, UserUpdateModel


class UserRepository(SQLAlchemyRepository):
    model = UserModel


class UserBuildingRepository(SQLAlchemyRepository):
    model = UserBuildingModel


class UserUpdateRepository(SQLAlchemyRepository):
    model = UserUpdateModel
