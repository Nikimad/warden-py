import asyncio
import sys

from .fetch import fetch


def main() -> None:
    url = sys.argv[1]
    result = asyncio.run(fetch(url))

    if result.content is None:
        print(f"ERROR | {url} | {result.error}")
    else:
        print(f"OK | {url} | {result.status_code} | {len(result.content)} bytes")
