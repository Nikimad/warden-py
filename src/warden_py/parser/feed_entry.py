from dataclasses import dataclass


@dataclass(frozen=True)
class FeedEntry:  # TS: Readonly<{ url, title, description, imageUrl: string | null }>
    url: str  # entry["link"]
    title: str  # entry["title"]
    description: str  # entry["summary"]
    image_url: str | None = None
