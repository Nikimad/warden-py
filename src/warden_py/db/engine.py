from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from .models import Base


def create_db_engine(url: str) -> AsyncEngine:
    return create_async_engine(url)


async def create_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
