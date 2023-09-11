# import yaml

import asyncio
import re

from .repo import Repository


async def _check_has_readme(repo: Repository) -> bool:
    for file in repo.files:
        if match := re.search("^(copying|readme)(|.md|.txt)$", file, re.IGNORECASE):
            print(f"{repo.name} has a readme ({match.string})")
            return False

    print(f"{repo.name} doesn't have a readme")
    return True


# def raw_url(repo: str, path: str) -> str:
#     return f"https://raw.githubusercontent.com/{repo}/HEAD/{path}"


async def _check_precommit(repo: Repository) -> bool:
    # async with github.get_async_client() as client:
    #     resp = await client.get(raw_url(repo, item.path))
    #     resp.raise_for_status()

    #     print(resp.content)
    #     config = yaml.safe_load(resp.content)
    #     print(config)
    ret = ".pre-commit-config.yaml" not in repo.files
    if ret:
        print(f"{repo.name} not using pre-commit")
    else:
        print(f"{repo.name} using pre-commit")

    return ret


_checks = (
    _check_has_readme,
    _check_precommit,
)


async def run_checks(repo_name: str) -> None:
    repo = await Repository.from_name(repo_name)
    if repo.language != "Python":
        raise RuntimeError("Python is currently the only supported language")

    futures = (check(repo) for check in _checks)
    have_suggestions = any(await asyncio.gather(*futures))
    if not have_suggestions:
        print("We have no suggestions to make. Well done :-)")
