import datetime

from models import Base, build_id, created_at, time_1971, updated_at, user_id
from sqlalchemy import DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from user.schemas import (
    UserBuildingSchema,
    UserReferalsSchema,
    UserSchema,
    UserUpdateSchema,
)


class UserModel(Base):
    __tablename__ = "users"
    first_name: Mapped[str]
    last_name: Mapped[str]
    username: Mapped[str]
    balance: Mapped[int] = mapped_column(default=0)
    income: Mapped[int] = mapped_column(default=0)
    level: Mapped[int] = mapped_column(default=1)
    referals: Mapped[int] = mapped_column(default=0)

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
            level=self.level,
            referals=self.referals,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class UserBuildingModel(Base):
    __tablename__ = "user_buildings"
    user_id: Mapped[user_id]
    build_id: Mapped[build_id]
    last_used_at: Mapped[time_1971]

    __table_args__ = (UniqueConstraint("user_id", "build_id", name="uq_user_building"),)

    def to_read_model(self):
        return UserBuildingSchema(
            id=self.id,
            user_id=self.user_id,
            building_id=self.build_id,
            last_used_at=self.last_used_at,
        )


class UserUpdateModel(Base):
    __tablename__ = "user_update"
    user_id: Mapped[user_id]
    last_earn_daily: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc)
        - datetime.timedelta(days=1, hours=1),
    )
    last_earn_debit_card: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc)
        - datetime.timedelta(days=1, hours=1),
    )

    def to_read_model(self):
        return UserUpdateSchema(
            id=self.id,
            user_id=self.user_id,
            last_earn_daily=self.last_earn_daily,
            last_earn_debit_card=self.last_earn_debit_card,
        )


class UserReferalModel(Base):
    __tablename__ = "user_referals"
    referer_id: Mapped[user_id]
    referal_id: Mapped[user_id]

    def to_read_model(self):
        return UserReferalsSchema(referer_id=self.referer_id, referal_id=self.referal_id)
