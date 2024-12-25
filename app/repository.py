from abc import ABC, abstractmethod
from typing import Callable

from models import Base
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class AbstractRepository(ABC):
    @abstractmethod
    def __init__(self, session: Callable) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, id: int) -> list:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> list:
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, data: dict) -> int:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id: int, data: dict) -> list:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int) -> int:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model: type[Base]

    def __init__(self, session: async_sessionmaker[AsyncSession]) -> None:
        self.session: AsyncSession = session()

    async def find_one(self, id: int) -> list:
        stmt = select(self.model).filter_by(id=id)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res

    async def find_all(self) -> list:
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res

    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalar_one()

    async def update_one(self, id: int, data: dict) -> list:
        stmt = (
            update(self.model)
            .values(**data)
            .where(self.model.id == id)
            .returning(self.model)
        )
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        await self.session.commit()
        return res

    async def delete_one(self, id: int) -> int:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model.id)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalar_one()