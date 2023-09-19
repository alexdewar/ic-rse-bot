import yaml

from ic_rse_bot.checks import BaseCheck
from ic_rse_bot.repo import Repository, github

_Hooks = dict[str, set[str]]
_RECOMMENDED_HOOKS: _Hooks = {
    "https://github.com/pre-commit/pre-commit-hooks": {
        "check-merge-conflict",
        "debug-statements",
    },
    "https://github.com/asottile/pyupgrade": {"pyupgrade"},
    "https://github.com/PyCQA/autoflake": {"autoflake"},
    "https://github.com/pycqa/isort": {"isort"},
    "https://github.com/psf/black": {"black"},
    "https://github.com/PyCQA/flake8": {"flake8"},
    "https://github.com/pre-commit/mirrors-mypy": {"mypy"},
    "https://github.com/igorshubovych/markdownlint-cli": {"markdownlint"},
}

_NO_PRECOMMIT_MSG = (
    "It seems you are not using pre-commit. Pre-commit is a useful "
    "tool which runs a set of extra checks before you commit to your git repository. "
    "This helps you catch errors and stylistic problems early in development. For more "
    "information, please consult the [pre-commit website](https://pre-commit.com/)."
    "\n\n"
)

_SUGGESTED_HOOKS_MSG = (
    "While it seems that you have pre-commit installed, we found some extra hooks you "
    "might consider installing.\n\n"
)


def _raw_url(repo: Repository, path: str) -> str:
    return f"https://raw.githubusercontent.com/{repo.full_name}/HEAD/{path}"


async def _get_precommit_hooks(repo: Repository) -> _Hooks:
    async with github.get_async_client() as client:
        resp = await client.get(_raw_url(repo, ".pre-commit-config.yaml"))
        resp.raise_for_status()

    config = yaml.safe_load(resp.content)
    hooks: _Hooks = {}
    for hook_repo in config["repos"]:
        hooks[hook_repo["repo"]] = {hook["id"] for hook in hook_repo["hooks"]}
    return hooks


async def _get_suggested_hooks(repo: Repository) -> _Hooks:
    current_hooks = await _get_precommit_hooks(repo)
    suggested_hooks: _Hooks = {}
    for url, ids in _RECOMMENDED_HOOKS.items():
        # If the user already has some of the hooks installed, ignore these ones
        if url in current_hooks:
            ids = ids.difference(current_hooks[url])

        if ids:
            suggested_hooks[url] = ids
    return suggested_hooks


class CheckPreCommit(BaseCheck):
    def __init__(self) -> None:
        super().__init__("Pre-commit", "Add pre-commit hooks")

    async def run(self, repo: Repository) -> str | None:
        msg = ""

        has_precommit = ".pre-commit-config.yaml" in repo.files
        if not has_precommit:
            msg += _NO_PRECOMMIT_MSG

        if suggested_hooks := await _get_suggested_hooks(repo):
            if has_precommit:
                msg += _SUGGESTED_HOOKS_MSG

            msg += "Suggested hooks (IDs in brackets):\n\n"
            for url, ids in suggested_hooks.items():
                msg += f"* {url} ({', '.join(sorted(ids))})\n"

        return msg if msg else None
