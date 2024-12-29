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
    created_at: datetime
    updated_at: datetime


class UserBalanceSchema(BaseModel):
    user_id: int
    balance: int
    income: int


class UserCardModel(BaseModel):
    id: int
    user_id: int
    card_name: str
    last_used_at: datetime


class GetUserSchema(BaseModel):
    user: UserSchema
