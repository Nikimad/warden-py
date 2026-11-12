from typing import Any

import pytest

from warden_py.parser import FeedEntry, extract_image_url, parse_feed

RSS = b"""<?xml version="1.0"?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
  <channel>
    <title>Test</title>
    <item>
      <title>Full</title>
      <link>https://news.test/full</link>
      <description>Text</description>
      <media:thumbnail url="https://img.test/full.jpg" width="240" />
    </item>
    <item>
      <title>No description, no image</title>
      <link>https://news.test/bare</link>
    </item>
    <item>
      <title>No link</title>
    </item>
    <item>
      <link>https://news.test/no-title</link>
    </item>
  </channel>
</rss>
"""

IMAGE_CASES = [
    pytest.param(
        {
            "media_content": [
                {"url": "https://img.test/140.jpg", "width": "140"},
                {"url": "https://img.test/700.jpg", "width": "700"},
                {"url": "https://img.test/460.jpg", "width": "460"},
            ]
        },
        "https://img.test/700.jpg",
        id="media_content_widest",
    ),
    pytest.param(
        {
            "media_content": [{"url": "https://img.test/content.jpg", "medium": "image"}],
            "media_thumbnail": [{"url": "https://img.test/thumb.jpg"}],
        },
        "https://img.test/content.jpg",
        id="media_content_before_thumbnail",
    ),
    pytest.param(
        {"media_thumbnail": [{"url": "https://img.test/thumb.jpg", "width": "240"}]},
        "https://img.test/thumb.jpg",
        id="media_thumbnail",
    ),
    pytest.param(
        {"enclosures": [{"href": "https://img.test/enc.jpg", "type": "image/jpg"}]},
        "https://img.test/enc.jpg",
        id="enclosure_image",
    ),
    pytest.param(
        {"enclosures": [{"href": "https://audio.test/ep.mp3", "type": "audio/mpeg"}]},
        None,
        id="enclosure_not_image",
    ),
    pytest.param({}, None, id="no_image"),
]


@pytest.mark.parametrize(("entry", "expected"), IMAGE_CASES)
def test_extract_image_url(entry: dict[str, Any], expected: str | None) -> None:
    assert extract_image_url(entry) == expected


def test_parse_feed() -> None:
    assert parse_feed(RSS) == [
        FeedEntry(
            url="https://news.test/full",
            title="Full",
            description="Text",
            image_url="https://img.test/full.jpg",
        ),
        FeedEntry(
            url="https://news.test/bare",
            title="No description, no image",
            description="",
        ),
    ]


def test_parse_feed_not_a_feed() -> None:
    assert parse_feed(b"<html><body>Not a feed</body></html>") == []
