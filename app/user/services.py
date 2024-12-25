from database import async_session_maker
from repository import AbstractRepository

from user.schemas import ResponseBalanceSchema, UserAddSchema, UserSchema


class UserService:
    def __init__(self, repository: type[AbstractRepository]) -> None:
        self.repository: AbstractRepository = repository(async_session_maker)

    async def add_user(self, user: UserAddSchema) -> int:
        user_dict = user.model_dump()
        user_id = await self.repository.add_one(user_dict)
        return user_id

    async def get_balance(self, user_id: int) -> ResponseBalanceSchema:
        response = await self.repository.find_one(id=user_id)[0]
        return ResponseBalanceSchema(
            balance=response.balance,
            raise_in_hours=response.raise_in_hours,
        )

    async def get_user(self, user_id: int) -> UserSchema:
        response = await self.repository.find_one(id=user_id)
        response = response[0]
        return UserSchema(
            id=response.id,
            first_name=response.first_name,
            last_name=response.last_name,
            username=response.username,
            balance=response.balance,
            raise_in_hours=response.raise_in_hours,
        )
