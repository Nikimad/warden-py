from typing import Any


def extract_image_url_from_enclosures(enclosures: list[dict[str, Any]]) -> str | None:
    for enclosure in enclosures:
        if enclosure.get("type", "").startswith("image/"):
            href: str | None = enclosure.get("href")
            if href:
                return href

    return None
