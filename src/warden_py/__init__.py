import asyncio
import sys

from .checker import check
from .formatter import format_result


def main() -> None:
    url = sys.argv[1]
    result = asyncio.run(check(url))
    print(format_result(result))
