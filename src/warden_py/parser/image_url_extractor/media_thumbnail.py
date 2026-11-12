from typing import Any


def extract_image_url_from_media_thumbnail(
    media_thumbnail: list[dict[str, Any]],
) -> str | None:
    return media_thumbnail[0].get("url") if media_thumbnail else None
