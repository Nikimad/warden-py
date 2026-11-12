from typing import Any


def extract_image_url_from_media_content(media_content: list[dict[str, Any]]) -> str | None:
    url = None
    max_width = 0

    for content in media_content:
        content_url = content.get("url")

        if not content_url:
            continue

        try:
            content_width = int(content.get("width") or 1)
        except ValueError, TypeError:
            content_width = 1

        if content_width > max_width:
            url = content_url
            max_width = content_width

    return url
