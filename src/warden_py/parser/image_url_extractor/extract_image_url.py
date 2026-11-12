from typing import Any

from warden_py.parser.image_url_extractor.enclosures import extract_image_url_from_enclosures
from warden_py.parser.image_url_extractor.media_content import extract_image_url_from_media_content
from warden_py.parser.image_url_extractor.media_thumbnail import (
    extract_image_url_from_media_thumbnail,
)

EXTRACTORS = [
    ("media_content", extract_image_url_from_media_content),
    ("media_thumbnail", extract_image_url_from_media_thumbnail),
    ("enclosures", extract_image_url_from_enclosures),
]


def extract_image_url(entry: dict[str, Any]) -> str | None:
    for source, extractor in EXTRACTORS:
        if source not in entry:
            continue

        url = extractor(entry[source])
        if url is not None:
            return url

    return None
