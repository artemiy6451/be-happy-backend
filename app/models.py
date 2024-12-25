import datetime
from typing import Annotated

from sqlalchemy import Integer, MetaData, text
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


class Base(DeclarativeBase):
    id: Mapped[idpk]
