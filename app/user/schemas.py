from pydantic import BaseModel


class UserAddSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str


class UserSchema(UserAddSchema):
    balance: int
    raise_in_hours: int


class ResponseBalanceSchema(BaseModel):
    balance: int
    raise_in_hours: int
