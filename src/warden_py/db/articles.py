from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncEngine

from warden_py.parser import FeedEntry

from .models import Article


async def save_articles(engine: AsyncEngine, entries: list[FeedEntry]) -> int:
    if not entries:
        return 0

    rows = [
        {
            "url": entry.url,
            "title": entry.title,
            "description": entry.description,
            "image_url": entry.image_url,
        }
        for entry in entries
    ]

    stmt = insert(Article).values(rows).on_conflict_do_nothing(index_elements=["url"])

    async with engine.begin() as conn:
        result = await conn.execute(stmt)

    return result.rowcount
