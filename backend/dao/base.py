from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, insert, update, delete, asc, desc
from sqlalchemy.ext.asyncio import async_session

from backend.database import async_session_maker
from backend.products.models import Products


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
    async def get_all(cls, search: Optional[str] = None, sort_by: Optional[str] = None):
        async with async_session_maker() as session:
            query = select(Products)
            if search:
                query = query.where(Products.name.ilike(f"%{search}%"))
            if sort_by:
                if sort_by == "asc":
                    query = query.order_by(asc(Products.price))
                elif sort_by == "desc":
                    query = query.order_by(desc(Products.price))
            result = await session.execute(query)
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

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        try:
            query = insert(cls.model).values(**data).returning(cls.model.id)
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
    async def purchase_product(cls, product_id: int):
        try:
            async with async_session_maker() as session:
                stmt = delete(cls.model).where(cls.model.id == product_id)
                await session.execute(stmt)
                await session.commit()
                return {"status": "success", "message": "Product purchased and deleted successfully"}
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot delete product"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot delete product"
            return {"status": "error", "message": msg}
