from typing import Annotated

from fastapi import APIRouter, Depends, status

from user.dependencies import user_service
from user.schemas import (
    GetUserSchema,
    UserBalanceSchema,
    UserBuildingSchema,
)
from user.services import AddUserSchema, UserService

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post(
    "/add_user",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": GetUserSchema},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "User already created."},
    },
)
async def add_user(
    user_data: AddUserSchema,
    service: Annotated[UserService, Depends(user_service)],
):
    user = await service.add_user(user_data)
    return GetUserSchema(user=user)


@user_router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": GetUserSchema},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
async def get_user(
    id: int,
    service: Annotated[UserService, Depends(user_service)],
):
    user = await service.get_user(id)
    return GetUserSchema(user=user)


@user_router.get(
    "/{user_id}/balance",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": UserBalanceSchema},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
async def get_balance(
    user_id: int,
    service: Annotated[UserService, Depends(user_service)],
):
    response = await service.get_balance(user_id)
    return response


@user_router.post(
    "/{user_id}/earn_daily",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": UserBalanceSchema},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
async def earn_daily(
    user_id: int,
    service: Annotated[UserService, Depends(user_service)],
):
    balance = await service.earn(user_id)
    return balance


@user_router.post(
    "/{user_id}/buy_building",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": UserBalanceSchema},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
async def buy_building(
    user_id: int,
    building_id: int,
    service: Annotated[UserService, Depends(user_service)],
):
    balance = await service.buy_building(user_id, building_id)
    return balance


@user_router.get(
    "/{user_id}/get_buildings",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": list[UserBuildingSchema]},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
async def get_buildings(
    user_id: int,
    service: Annotated[UserService, Depends(user_service)],
):
    buildings = await service.get_user_buildings(user_id)
    return buildings


@user_router.post(
    "/{user_id}/earn_by_click",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": UserBalanceSchema},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
async def earn_by_click(
    user_id: int,
    service: Annotated[UserService, Depends(user_service)],
):
    balance = await service.earn_by_click(user_id)
    return balance
