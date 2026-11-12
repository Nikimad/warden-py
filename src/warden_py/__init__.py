import asyncio

from warden_py.parser import parse_feed

from .config import load_feed_urls
from .download import download_feeds


def main() -> None:
    results = asyncio.run(download_feeds(load_feed_urls()))

    for result in results:
        if result.content is None:
            print(f"ERROR | {result.url} | {result.error}")
        else:
            feed = parse_feed(result.content)
            print(feed)
