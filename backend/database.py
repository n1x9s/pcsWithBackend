from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker

from backend.config import settings


DATABASE_URL = settings.DATABASE_URL
DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

# Во 2.0 версии Алхимии был добавлен async_sessionamaker.
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
