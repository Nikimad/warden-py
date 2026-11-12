import feedparser

from warden_py.parser.feed_entry import FeedEntry
from warden_py.parser.image_url_extractor import extract_image_url


def parse_feed(content: bytes) -> list[FeedEntry]:
    entries = feedparser.parse(content).entries

    return [
        FeedEntry(
            url=entry["link"],
            title=entry["title"],
            description=entry.get("summary") or "",
            image_url=extract_image_url(entry),
        )
        for entry in entries
        if entry.get("link") and entry.get("title")
    ]
