from models import Base, created_at, updated_at
from sqlalchemy.orm import Mapped, mapped_column

from user.schemas import UserSchema


class UserModel(Base):
    __tablename__ = "users"
    first_name: Mapped[str]
    last_name: Mapped[str]
    username: Mapped[str]

    balance: Mapped[int] = mapped_column(default=0)
    raise_in_hour: Mapped[int] = mapped_column(default=0)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    def to_read_model(self):
        return UserSchema(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
            balance=self.balance,
            raise_in_hours=self.raise_in_hour,
        )
