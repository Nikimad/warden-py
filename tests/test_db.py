from collections.abc import AsyncIterator

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine

from warden_py.db import create_db_engine, create_tables, save_articles
from warden_py.parser import FeedEntry

ENTRIES = [
    FeedEntry(url="https://example.test/a", title="A", description="First"),
    FeedEntry(
        url="https://example.test/b",
        title="B",
        description="Second",
        image_url="https://example.test/b.jpg",
    ),
]


@pytest.fixture
async def engine() -> AsyncIterator[AsyncEngine]:
    engine = create_db_engine("sqlite+aiosqlite:///:memory:")
    await create_tables(engine)
    yield engine
    await engine.dispose()


async def test_save_articles_new(engine: AsyncEngine) -> None:
    assert await save_articles(engine, ENTRIES) == len(ENTRIES)


async def test_save_articles_skips_duplicates(engine: AsyncEngine) -> None:
    await save_articles(engine, ENTRIES)

    assert await save_articles(engine, ENTRIES) == 0
