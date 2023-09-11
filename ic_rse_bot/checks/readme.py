import re

from ic_rse_bot.repo import Repository


async def run_check(repo: Repository) -> str | None:
    for file in repo.files:
        if re.search("^(copying|readme)(|.md|.txt)$", file, re.IGNORECASE):
            return None

    return "You should consider adding a readme"
