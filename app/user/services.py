from database import async_session_maker
from fastapi import HTTPException
from repository import AbstractRepository
from sqlalchemy.exc import IntegrityError
from starlette import status

from user.models import UserModel
from user.schemas import (
    AddUserSchema,
    UserBalanceSchema,
    UserSchema,
)


class UserService:
    def __init__(self, repository: type[AbstractRepository]) -> None:
        self.repository: AbstractRepository = repository(async_session_maker)

    async def add_user(self, user_data: AddUserSchema) -> UserSchema:
        try:
            user_dict = user_data.model_dump()
            user_id: int = await self.repository.add_one(user_dict)
            response: UserModel = await self.repository.find_one(id=user_id)
            if response is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Can not get user with id: {user_id}",
                )
            user = response.to_read_model()
            return user
        except IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User already created.",
            ) from exc

    async def get_user(self, user_id: int) -> UserSchema:
        response: UserModel = await self.repository.find_one(id=user_id)
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Can not get user with id: {user_id}",
            )
        user = response.to_read_model()
        return user

    async def get_balance(self, user_id: int) -> UserBalanceSchema:
        response: UserModel = await self.repository.find_one(id=user_id)
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Can not get user with id: {user_id}",
            )
        user = response.to_read_model()
        return UserBalanceSchema(
            user_id=user.id, balance=user.balance, income=user.income
        )
