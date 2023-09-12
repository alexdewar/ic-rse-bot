import re

from ic_rse_bot.checks import BaseCheck
from ic_rse_bot.repo import Repository


class ReadmeCheck(BaseCheck):
    def __init__(self) -> None:
        super().__init__("Readme", "Add a readme file")

    async def run(self, repo: Repository) -> str | None:
        for file in repo.files:
            if re.search("^(copying|readme)(|.md|.txt)$", file, re.IGNORECASE):
                return None

        return "You should consider adding a readme file."
