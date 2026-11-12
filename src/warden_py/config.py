from pathlib import Path

import yaml

from .constants import SOURCES_PATH


def load_feed_urls(path: Path = SOURCES_PATH) -> list[str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return [str(feed["url"]) for feed in data["feeds"]]
