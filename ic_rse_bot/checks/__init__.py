import asyncio
import importlib
import pkgutil
import sys
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from ic_rse_bot.repo import Repository


@dataclass
class Check:
    name: str
    run: Callable[[Repository], Awaitable[str | None]]


def _get_checks() -> list[Check]:
    checks: list[Check] = []
    for info in pkgutil.iter_modules(sys.modules[__name__].__path__):
        module = importlib.import_module(f"{__name__}.{info.name}")
        checks.append(Check(info.name, module.run_check))
    return checks


_checks = _get_checks()


async def run_checks(repo_name: str) -> None:
    repo = await Repository.from_name(repo_name)
    if repo.language != "Python":
        raise RuntimeError("Python is currently the only supported language")

    check_names = [check.name for check in _checks]
    print(f"Running the following checks: {', '.join(check_names)}")

    futures = (check.run(repo) for check in _checks)
    results = await asyncio.gather(*futures)
    suggestions: list[tuple[str, str]] = [
        (name, msg) for name, msg in zip(check_names, results) if msg
    ]
    if not suggestions:
        print("We have no suggestions to make. Well done :-)")
        return

    print("We have the following suggestions:")
    for name, msg in suggestions:
        print(f"- {name}: {msg}")
