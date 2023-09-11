from __future__ import annotations

from typing import Any

from githubkit import GitHub, UnauthAuthStrategy
from githubkit.rest import FullRepository

github = GitHub()
github = GitHub(UnauthAuthStrategy())


class Repository:
    def __init__(self, repo: FullRepository, files: set[str]) -> None:
        self._repo = repo
        self.files = files

    def __getattribute__(self, name: str) -> Any:
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return getattr(self._repo, name)

    @staticmethod
    async def from_name(name: str) -> Repository:
        owner, repo = name.split("/")
        repo_resp = await github.rest.repos.async_get(owner, repo)

        # TODO: Don't hardcode tree_sha arg
        tree_resp = await github.rest.git.async_get_tree(
            owner, repo, tree_sha="HEAD", recursive=True
        )
        files = {item.path for item in tree_resp.parsed_data.tree}

        return Repository(repo_resp.parsed_data, files)


# async def get_latest_commit(repo: str):
#     github.rest.git.get_tree()
#     github.get_async_client()
#     owner, repo = repo.split("/")
#     resp = await github.rest.repos.async_get_commit(owner, repo, "HEAD")
#     return resp.parsed_data
