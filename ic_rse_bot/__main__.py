"""The entry point for the bot program."""
import asyncio
import sys

from .checks import run_checks


async def main() -> None:
    if len(sys.argv) != 2:
        raise RuntimeError("Repo name must be provided")

    await run_checks(sys.argv[1])


if __name__ == "__main__":
    asyncio.run(main())
