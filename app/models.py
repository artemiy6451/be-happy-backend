import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, Integer, MetaData, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

metadata = MetaData()

created_at = Annotated[
    datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
    ),
]

idpk = Annotated[int, mapped_column(Integer, primary_key=True)]


def default_1971() -> datetime.datetime:
    return datetime.datetime(1971, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)


time_1971 = Annotated[
    datetime.datetime,
    mapped_column(
        default=default_1971,
    ),
]

user_id = Annotated[int, mapped_column(ForeignKey("users.id", ondelete="CASCADE"))]


class Base(DeclarativeBase):
    id: Mapped[idpk]
