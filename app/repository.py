from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, Optional, Type, TypeVar

from models import Base
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

T = TypeVar("T", bound=Base)


class AbstractRepository(ABC):
    @abstractmethod
    def __init__(self, session: Callable) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, id: int) -> Base | None:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, filter_by: Optional[Any]) -> list:
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


class SQLAlchemyRepository(AbstractRepository, Generic[T]):
    model: Type[T]

    def __init__(self, session: async_sessionmaker[AsyncSession]) -> None:
        self.session: AsyncSession = session()

    async def find_one(self, id: int) -> T | None:
        stmt = select(self.model).filter_by(id=id)
        res = await self.session.execute(stmt)
        row = res.scalar_one_or_none()
        return row

    async def find_all(
        self,
        filter_by: Optional[Any] = None,
        join_by: Optional[tuple[Any, Any, Any]] = None,
    ) -> list[T]:
        stmt = select(self.model)
        if join_by:
            stmt = select(self.model, join_by[1])
            stmt = stmt.select_from(join_by[0]).join(*join_by[1:])
        if filter_by is not None:
            stmt = stmt.where(filter_by)
        if join_by:
            res = await self.session.execute(stmt)
            res = list(res.all())
            return res

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
        return res[0]

    async def delete_one(self, id: int) -> int:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model.id)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalar_one()
