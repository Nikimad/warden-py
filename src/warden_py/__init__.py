import asyncio

from dotenv import load_dotenv

from .config import load_database_url, load_feed_urls
from .db import create_db_engine, create_tables, save_articles
from .download import download_feeds
from .parser import parse_feed


async def run() -> None:
    database_url = load_database_url()
    feeds_urls = load_feed_urls()
    engine = create_db_engine(database_url)

    try:
        await create_tables(engine)
        feeds = await download_feeds(feeds_urls)

        for feed in feeds:
            if feed.content is None:
                print(f"ERROR | {feed.url} | {feed.error}")
                continue

            entries = parse_feed(feed.content)
            count = await save_articles(engine, entries)
            print(f"OK    | {feed.url} | new: {count} of {len(entries)}")
    finally:
        await engine.dispose()


def main() -> None:
    load_dotenv()
    asyncio.run(run())
