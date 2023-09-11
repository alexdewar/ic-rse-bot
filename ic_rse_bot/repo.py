from __future__ import annotations

from typing import Any

from githubkit import GitHub, UnauthAuthStrategy
from githubkit.rest import FullRepository

github = GitHub()
github = GitHub(UnauthAuthStrategy())


class Repository:
    def __init__(self, repo: FullRepository) -> None:
        self._repo = repo
        self._files: set[str]

    def __getattribute__(self, name: str) -> Any:
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return getattr(self._repo, name)

    @property
    async def files(self) -> set[str]:
        if hasattr(self, "_files"):
            return self._files

        # TODO: Don't hardcode tree_sha arg
        resp = await github.rest.git.async_get_tree(
            self._repo.owner.login,
            self._repo.name,
            tree_sha="HEAD",
            recursive=True,
        )
        self._files = {item.path for item in resp.parsed_data.tree}
        return self._files

    async def from_name(name: str) -> Repository:
        owner, repo = name.split("/")
        resp = await github.rest.repos.async_get(owner, repo)
        return Repository(resp.parsed_data)


# async def get_latest_commit(repo: str):
#     github.rest.git.get_tree()
#     github.get_async_client()
#     owner, repo = repo.split("/")
#     resp = await github.rest.repos.async_get_commit(owner, repo, "HEAD")
#     return resp.parsed_data
