import datetime
from typing import Annotated

from sqlalchemy import BigInteger, DateTime, ForeignKey, MetaData, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

metadata = MetaData()

created_at = Annotated[
    datetime.datetime,
    mapped_column(
        DateTime(timezone=True), server_default=text("TIMEZONE('utc', now())")
    ),
]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
    ),
]

idpk = Annotated[int, mapped_column(BigInteger, primary_key=True)]


def default_1971() -> datetime.datetime:
    return datetime.datetime(1971, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)


time_1971 = Annotated[
    datetime.datetime,
    mapped_column(
        DateTime(timezone=True),
        default=default_1971,
        onupdate=datetime.datetime.now(datetime.timezone.utc),
    ),
]

user_id = Annotated[int, mapped_column(ForeignKey("users.id", ondelete="CASCADE"))]
build_id = Annotated[int, mapped_column(ForeignKey("buildings.id", ondelete="CASCADE"))]


class Base(DeclarativeBase):
    id: Mapped[idpk]
