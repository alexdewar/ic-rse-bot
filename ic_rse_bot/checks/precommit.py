from ic_rse_bot.checks import BaseCheck
from ic_rse_bot.repo import Repository


class CheckPreCommit(BaseCheck):
    def __init__(self) -> None:
        super().__init__("Pre-commit", "Add pre-commit hooks")

    async def run(self, repo: Repository) -> str | None:
        if ".pre-commit-config.yaml" not in repo.files:
            return "You should consider using pre-commit"

        return None
