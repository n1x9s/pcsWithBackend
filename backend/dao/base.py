from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, insert, update, delete

from backend.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def create(cls, **data):
        try:
            query = insert(cls.model).values(**data)
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.mappings().first()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot insert data into table"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot insert data into table"
            return None

    @classmethod
    async def get_all(cls):
        async with async_session_maker() as session:
            stmt = select(cls.model)
            result = await session.execute(stmt)
            return result.scalars().all()

    @classmethod
    async def get_by_id(cls, id):
        async with async_session_maker() as session:
            stmt = select(cls.model).filter(cls.model.id == id)
            result = await session.execute(stmt)
            return result.scalars().first()

    @classmethod
    async def update(cls, id, **kwargs):
        async with async_session_maker() as session:
            async with session.begin():
                stmt = update(cls.model).where(cls.model.id == id).values(**kwargs)
                await session.execute(stmt)
                await session.commit()

    @classmethod
    async def delete(cls, id):
        async with async_session_maker() as session:
            async with session.begin():
                stmt = delete(cls.model).where(cls.model.id == id)
                await session.execute(stmt)
                await session.commit()
