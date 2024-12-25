from user.repository import UserRepository
from user.services import UserService


def user_service():
    return UserService(UserRepository)
