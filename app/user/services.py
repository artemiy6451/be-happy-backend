import datetime

from city.models import BuildingModel
from city.repository import CityRepository
from config import Settings
from database import async_session_maker
from fastapi import HTTPException
from repository import AbstractRepository
from sqlalchemy.exc import IntegrityError
from starlette import status
from telegram_webapp_auth.auth import TelegramUser

from user.models import UserBuildingModel, UserModel, UserReferalModel, UserUpdateModel
from user.repository import (
    UserBuildingRepository,
    UserReferalRepository,
    UserUpdateRepository,
)
from user.schemas import (
    AddUserSchema,
    UserBalanceSchema,
    UserBuildingWithNamesSchema,
    UserSchema,
    UserUpdateSchema,
)


class UserService:
    def __init__(self, repository: type[AbstractRepository]) -> None:
        self.user_repository: AbstractRepository = repository(async_session_maker)
        self.user_buildings_repository: AbstractRepository = UserBuildingRepository(
            async_session_maker
        )
        self.user_update_repository: AbstractRepository = UserUpdateRepository(
            async_session_maker
        )
        self.user_referal_repository: AbstractRepository = UserReferalRepository(
            async_session_maker
        )

    async def add_user(self, user_data: TelegramUser) -> UserSchema:
        try:
            user = AddUserSchema(
                id=user_data.id,
                first_name=user_data.first_name,
                last_name=user_data.last_name if user_data.last_name else "",
                username=user_data.username if user_data.username else "",
            )
            user_dict = user.model_dump()
            user_id: int = await self.user_repository.add_one(user_dict)
            data = {"user_id": user_id}
            await self.user_update_repository.add_one(data)

            user_model: UserModel = await self.user_repository.find_one(id=user_id)
            if user_model is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Can not get user with id: {user_id}",
                )
            user = user_model.to_read_model()
            return user
        except IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User already created.",
            ) from exc

    async def get_user(self, user_id: int) -> UserSchema:
        # TODO: вынести проверку пользователя в отдельную функцию на рефакторинге
        response: UserModel = await self.user_repository.find_one(id=user_id)
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Can not get user with id: {user_id}",
            )
        user = response.to_read_model()
        return user

    async def get_balance(self, user_id: int) -> UserBalanceSchema:
        response: UserModel = await self.user_repository.find_one(id=user_id)
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Can not get user with id: {user_id}",
            )
        user = response.to_read_model()
        return UserBalanceSchema(
            user_id=user.id, balance=user.balance, income=user.income, level=user.level
        )

    async def earn(self, user_id: int) -> UserBalanceSchema:
        filter = UserUpdateModel.user_id == user_id
        update_time_list = await self.user_update_repository.find_all(filter)
        update_time = update_time_list[0]

        user_model: UserModel = await self.user_repository.find_one(id=user_id)
        if user_model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Can not get user with id: {user_id}",
            )
        user = user_model.to_read_model()

        now_utc = datetime.datetime.now(datetime.timezone.utc)

        if update_time.last_earn_daily.tzinfo is None:
            update_time.last_earn_daily = update_time.last_earn_daily.replace(
                tzinfo=datetime.timezone.utc
            )

        delta_in_hours = (now_utc - update_time.last_earn_daily).total_seconds() // 3600

        if not (delta_in_hours >= Settings().daily_reward_time):
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="Not ready.",
            )

        data = {"balance": user.balance + (user.income)}

        updated_user: UserSchema = await self.user_repository.update_one(
            id=user.id, data=data
        )
        data = {"last_earn_daily": datetime.datetime.now(datetime.timezone.utc)}
        await self.user_update_repository.update_one(id=update_time.id, data=data)
        return UserBalanceSchema(
            user_id=updated_user.id,
            balance=updated_user.balance,
            income=updated_user.income,
            level=updated_user.level,
        )

    async def earn_by_click(self, user_id: int) -> UserBalanceSchema:
        user_model: UserModel = await self.user_repository.find_one(id=user_id)
        if user_model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Can not get user with id: {user_id}",
            )
        user = user_model.to_read_model()
        new_balance = user.balance + Settings().earn_by_click_amount
        balance = await self.update_balance(user_id=user.id, new_balance=new_balance)
        return UserBalanceSchema(
            user_id=user.id, balance=balance, income=user.income, level=user.level
        )

    async def earn_debit_card(self, user_id: int) -> UserBalanceSchema:
        filter = UserUpdateModel.user_id == user_id
        update_time_list = await self.user_update_repository.find_all(filter)
        update_time = update_time_list[0]

        user_model: UserModel = await self.user_repository.find_one(id=user_id)
        if user_model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Can not get user with id: {user_id}",
            )
        user = user_model.to_read_model()

        now_utc = datetime.datetime.now(datetime.timezone.utc)

        if update_time.last_earn_debit_card.tzinfo is None:
            update_time.last_earn_debit_card = update_time.last_earn_debit_card.replace(
                tzinfo=datetime.timezone.utc
            )

        delta_in_hours = (
            now_utc - update_time.last_earn_debit_card
        ).total_seconds() // 3600

        if not (delta_in_hours >= Settings().card_reward_time):
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="Not ready.",
            )

        data = {"balance": user.balance + (Settings().earn_by_card_amount)}

        updated_user: UserSchema = await self.user_repository.update_one(
            id=user.id, data=data
        )
        data = {"last_earn_debit_card": datetime.datetime.now(datetime.timezone.utc)}
        await self.user_update_repository.update_one(id=update_time.id, data=data)
        return UserBalanceSchema(
            user_id=updated_user.id,
            balance=updated_user.balance,
            income=updated_user.income,
            level=updated_user.level,
        )

    async def update_balance(self, user_id: int, new_balance: int) -> int:
        # TODO: сделать проверку, чтобы нельзя было залить отрицательный баланс
        data = {"balance": new_balance}
        user = await self.user_repository.update_one(id=user_id, data=data)
        return user.balance

    async def update_income(self, user_id: int, new_income: int) -> int:
        # TODO: сделать проверку, чтобы нельзя было залить отрицательный баланс
        data = {
            "income": new_income,
        }
        user = await self.user_repository.update_one(id=user_id, data=data)
        return user.income

    async def update_level(self, user_id: int, new_level: int) -> int:
        data = {"level": new_level}
        user = await self.user_repository.update_one(id=user_id, data=data)
        return user.level

    async def buy_building(self, user_id: int, building_id: int) -> UserBalanceSchema:
        filter = (UserBuildingModel.user_id == user_id) & (
            UserBuildingModel.build_id == building_id
        )
        exist_user_building_list = await self.user_buildings_repository.find_all(filter)

        if exist_user_building_list:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Already exist."
            )

        city_repository: AbstractRepository = CityRepository(async_session_maker)
        balance = await self.get_balance(user_id)
        building = await city_repository.find_one(id=building_id)
        if building is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Building not found."
            )

        if balance.balance < building.cost:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="Not enough money.",
            )
        new_balance = balance.balance - building.cost
        new_income = balance.income + (
            building.income * balance.level * Settings().level_multiplier
        )
        new_level = balance.level + 1
        data = {
            "user_id": user_id,
            "build_id": building_id,
        }

        await self.user_buildings_repository.add_one(data)

        await self.update_income(user_id=user_id, new_income=new_income)
        await self.update_balance(user_id=user_id, new_balance=new_balance)
        await self.update_level(user_id=user_id, new_level=new_level)
        new_user_balance = await self.get_balance(user_id)
        return new_user_balance

    async def get_user_buildings(
        self, user_id: int
    ) -> list[UserBuildingWithNamesSchema]:
        filter = UserBuildingModel.user_id == user_id
        join = (
            UserBuildingModel,
            BuildingModel,
            UserBuildingModel.build_id == BuildingModel.id,
        )
        user_buildings: list[tuple[UserBuildingModel, BuildingModel]] = (
            await self.user_buildings_repository.find_all(filter, join)
        )

        buildings: list[UserBuildingWithNamesSchema] = []
        for user, building in user_buildings:
            buildings.append(
                UserBuildingWithNamesSchema(
                    user_id=user.user_id,
                    building_id=building.id,
                    name=building.name,
                    income=building.income,
                    cost=building.cost,
                    icon_url=building.icon_url,
                    last_used_at=user.last_used_at,
                )
            )

        return buildings

    async def get_updates(self, user_id: int) -> UserUpdateSchema:
        filter = UserUpdateModel.user_id == user_id
        user_model: UserModel = await self.user_repository.find_one(id=user_id)
        if user_model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Can not get user with id: {user_id}",
            )
        update_time_list = await self.user_update_repository.find_all(filter)
        return update_time_list[0]

    async def add_referal(self, referer_id: int, referal_id: int) -> UserSchema:
        if referer_id == referal_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Can not referal your own account",
            )

        filter = (UserReferalModel.referer_id == referer_id) & (
            UserReferalModel.referal_id == referal_id
        )
        referal = await self.user_referal_repository.find_all(filter)

        if referal:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You already referal this account",
            )

        filter = (UserReferalModel.referer_id == referal_id) & (
            UserReferalModel.referal_id == referer_id
        )
        referal = await self.user_referal_repository.find_all(filter)

        if referal:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You can not referal account that referal you",
            )

        referer_model: UserModel = await self.user_repository.find_one(id=referer_id)
        if referer_model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Can not get user with id: {referer_id}",
            )

        referal_model: UserModel = await self.user_repository.find_one(id=referal_id)
        if referal_model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Can not get user with id: {referer_id}",
            )
        referer_user = referer_model.to_read_model()
        referal_user = referal_model.to_read_model()

        data = {"referals": referer_user.referals + 1}
        referer_user = await self.user_repository.update_one(
            id=referer_user.id, data=data
        )
        data = {"referer_id": referer_id, "referal_id": referal_id}
        await self.user_referal_repository.add_one(data)

        return referal_user
