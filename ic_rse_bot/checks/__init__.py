import asyncio
import importlib
import pkgutil
import sys
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader

from ic_rse_bot.repo import Repository


@dataclass
class Check:
    name: str
    run: Callable[[Repository], Awaitable[str | None]]


@dataclass
class Suggestion:
    name: str
    content: str


def _get_checks() -> list[Check]:
    checks: list[Check] = []
    for info in pkgutil.iter_modules(sys.modules[__name__].__path__):
        module = importlib.import_module(f"{__name__}.{info.name}")
        checks.append(Check(info.name, module.run_check))
    return checks


async def _run_checks(repo: Repository) -> list[Suggestion]:
    checks = _get_checks()
    check_names = [check.name for check in checks]
    print(f"Running the following checks: {', '.join(check_names)}")

    futures = (check.run(repo) for check in checks)
    results = await asyncio.gather(*futures)
    suggestions: list[Suggestion] = [
        Suggestion(name, msg) for name, msg in zip(check_names, results) if msg
    ]
    return suggestions


def _apply_report_template(**kwargs: Any) -> str:
    file_loader = FileSystemLoader(Path(__file__).parent)
    env = Environment(loader=file_loader)
    template = env.get_template("report_template.md.jinja")
    return template.render(**kwargs)


async def generate_report(repo_name: str, report_path: Path) -> None:
    repo = await Repository.from_name(repo_name)
    if repo.language != "Python":
        raise RuntimeError("Python is currently the only supported language")

    suggestions = await _run_checks(repo)
    report = _apply_report_template(repo_name=repo_name, suggestions=suggestions)

    print(f"Saving report to {report_path}")
    with report_path.open("w") as file:
        file.write(report)

    print(f"The report is as follows:\n---------------------\n{report}", end="")
