from typing import Annotated

from fastapi import APIRouter, Depends, status
from schemas import SuccesAddSchema

from user.dependencies import user_service
from user.schemas import ResponseBalanceSchema, UserAddSchema
from user.services import UserService

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post(
    "/auth",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_201_CREATED: {"model": SuccesAddSchema}},
)
async def auth_user(
    user: UserAddSchema,
    service: Annotated[UserService, Depends(user_service)],
):
    id = await service.add_user(user)
    return SuccesAddSchema(id=id)

@user_router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"model": ResponseBalanceSchema}},
)
async def get_user(
    id: int,
    service: Annotated[UserService, Depends(user_service)],
):
    response = await service.get_user(id)
    return response


@user_router.get(
    "/{id}/balance",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"model": ResponseBalanceSchema}},
)
async def get_balance(
    id: int,
    service: Annotated[UserService, Depends(user_service)],
):
    response = await service.get_balance(id)
    return response
