from typing import Generator

from config import Settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

settings = Settings()


async_engine = create_async_engine(settings.database_uri)
async_session_maker = async_sessionmaker(async_engine)


def get_session() -> Generator[AsyncSession, None, None]:
    with async_session_maker() as session:  # type: ignore
        yield session
