"""The entry point for the bot program."""

import asyncio
import sys
from pathlib import Path

from .checks import generate_report

REPORT_PATH = "ic_rse_bot_report.md"


async def main() -> None:
    if len(sys.argv) != 2:
        raise RuntimeError("Repo name must be provided")

    await generate_report(sys.argv[1], Path(REPORT_PATH))


if __name__ == "__main__":
    asyncio.run(main())
