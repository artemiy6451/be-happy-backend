from typing import Annotated

from auth import get_current_user
from fastapi import APIRouter, Depends, status
from telegram_webapp_auth.auth import TelegramUser

from user.dependencies import user_service
from user.schemas import (
    GetUserSchema,
    UserBalanceSchema,
    UserBuildingWithNamesSchema,
)
from user.services import UserService

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
    service: Annotated[UserService, Depends(user_service)],
    user_data: TelegramUser = Depends(get_current_user),
):
    user = await service.add_user(user_data)
    return GetUserSchema(user=user)


@user_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": GetUserSchema},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
async def get_user(
    service: Annotated[UserService, Depends(user_service)],
    user_data: TelegramUser = Depends(get_current_user),
):
    user = await service.get_user(user_data.id)
    return GetUserSchema(user=user)


@user_router.get(
    "/balance",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": UserBalanceSchema},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
async def get_balance(
    service: Annotated[UserService, Depends(user_service)],
    user_data: TelegramUser = Depends(get_current_user),
):
    balance = await service.get_balance(user_data.id)
    return balance


@user_router.post(
    "/earn_daily",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": UserBalanceSchema},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
async def earn_daily(
    service: Annotated[UserService, Depends(user_service)],
    user_data: TelegramUser = Depends(get_current_user),
):
    balance = await service.earn(user_data.id)
    return balance


@user_router.post(
    "/buy_building",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": UserBalanceSchema},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
async def buy_building(
    building_id: int,
    service: Annotated[UserService, Depends(user_service)],
    user_data: TelegramUser = Depends(get_current_user),
):
    balance = await service.buy_building(user_data.id, building_id)
    return balance


@user_router.get(
    "/get_buildings",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": list[UserBuildingWithNamesSchema]},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
async def get_buildings(
    service: Annotated[UserService, Depends(user_service)],
    user_data: TelegramUser = Depends(get_current_user),
):
    buildings = await service.get_user_buildings(user_data.id)
    return buildings


@user_router.post(
    "/earn_by_click",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": UserBalanceSchema},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
async def earn_by_click(
    service: Annotated[UserService, Depends(user_service)],
    user_data: TelegramUser = Depends(get_current_user),
):
    balance = await service.earn_by_click(user_data.id)
    return balance
