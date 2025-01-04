from datetime import datetime

from pydantic import BaseModel


class AddUserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str


class UserSchema(AddUserSchema):
    balance: int
    income: int
    level: int
    referals: int
    created_at: datetime
    updated_at: datetime


class UserBalanceSchema(BaseModel):
    user_id: int
    balance: int
    income: int
    level: int


class UserBuildingSchema(BaseModel):
    id: int
    user_id: int
    building_id: int
    last_used_at: datetime


class UserBuildingWithNamesSchema(BaseModel):
    user_id: int
    building_id: int
    name: str
    income: int
    cost: int
    icon_url: str
    last_used_at: datetime


class UserUpdateSchema(BaseModel):
    id: int
    user_id: int
    last_earn_daily: datetime
    last_earn_debit_card: datetime


class UserReferalsSchema(BaseModel):
    referer_id: int
    referal_id: int


class AllReferalsSchema(BaseModel):
    user_id: int
    fristname: str
    referals: int


class GetUserSchema(BaseModel):
    user: UserSchema
