# app/db/database.py

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from app.core.config import settings

# -----------------------------
# 1. Create the async engine
# -----------------------------
engine = create_async_engine(
    settings.database_url,
    echo=False,            # Set True only for debugging SQL
    future=True
)

# -----------------------------
# 2. Create the async session factory
# -----------------------------
async_session = async_sessionmaker(
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    bind=engine,
    class_=AsyncSession,
)


# -----------------------------
# 3. Provide DB session to FastAPI routes
# -----------------------------
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for providing a SQLAlchemy AsyncSession.

    Using `yield` inside an async context manager automatically:
    - Opens session per request
    - Closes it after request
    """
    async with async_session() as session:
        yield session
