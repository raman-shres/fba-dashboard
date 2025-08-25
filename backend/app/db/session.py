# app/db/session.py

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# ✅ use absolute import so Pylance & runtime are happy
from app.config import settings


# Create the async engine (talks to Postgres via asyncpg)
engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,   # checks connections before using them
)

# Factory that gives us AsyncSession objects
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


# FastAPI dependency that yields a DB session and closes it afterward
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
