from models import Base, created_at, time_1971, updated_at, user_id
from sqlalchemy.orm import Mapped, mapped_column

from user.schemas import UserSchema


class UserModel(Base):
    __tablename__ = "users"
    first_name: Mapped[str]
    last_name: Mapped[str]
    username: Mapped[str]
    balance: Mapped[int] = mapped_column(default=0)
    income: Mapped[int] = mapped_column(default=0)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    def to_read_model(self):
        return UserSchema(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
            balance=self.balance,
            income=self.income,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class UserCardModel(Base):
    __tablename__ = "cards"
    user_id: Mapped[user_id]
    card_name: Mapped[str]
    last_used_at: Mapped[time_1971]

    def to_read_model(self):
        return UserCardModel(
            id=self.id,
            user_id=self.user_id,
            card_name=self.card_name,
            last_used_at=self.last_used_at,
        )
