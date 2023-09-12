import asyncio
import importlib
import inspect
import pkgutil
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader

from ic_rse_bot.repo import Repository


@dataclass
class Suggestion:
    heading: str
    content: str


class BaseCheck(ABC):
    def __init__(self, name: str, heading: str) -> None:
        self.name = name
        self.heading = heading

    @abstractmethod
    async def run(self, repo: Repository) -> str | None:
        pass


def _is_check_class(var: Any) -> bool:
    # If it's not a class at all, then it's not a check class
    if not inspect.isclass(var):
        return False

    # If var is actually BaseCheck itself, then it's not a check class
    if var is BaseCheck:
        return False

    # Finally check that var inherits from BaseCheck
    return issubclass(var, BaseCheck)


def _get_checks() -> list[BaseCheck]:
    checks: list[BaseCheck] = []

    # Iterate over submodules of ic_rse_bot.checks
    for info in pkgutil.iter_modules(sys.modules[__name__].__path__):
        # Import the submodule (TODO: Error handling)
        module = importlib.import_module(f"{__name__}.{info.name}")

        # Find any classes which inherit from BaseCheck
        for _, cls in inspect.getmembers(module, _is_check_class):
            # Create an instance of class
            checks.append(cls())

    return checks


async def _run_checks(repo: Repository) -> list[Suggestion]:
    checks = _get_checks()
    print(f"Running the following checks: {', '.join(check.name for check in checks)}")

    futures = (check.run(repo) for check in checks)
    results = await asyncio.gather(*futures)
    suggestions: list[Suggestion] = [
        Suggestion(check.heading, msg) for check, msg in zip(checks, results) if msg
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
