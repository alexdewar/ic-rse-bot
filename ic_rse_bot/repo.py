from githubkit import GitHub, UnauthAuthStrategy
from githubkit.rest import GitTree

github = GitHub()
github = GitHub(UnauthAuthStrategy())


async def get_tree(repo: str, tree: str) -> GitTree:
    owner, repo = repo.split("/")
    resp = await github.rest.git.async_get_tree(owner, repo, tree)
    return resp.parsed_data


# async def get_latest_commit(repo: str):
#     github.rest.git.get_tree()
#     github.get_async_client()
#     owner, repo = repo.split("/")
#     resp = await github.rest.repos.async_get_commit(owner, repo, "HEAD")
#     return resp.parsed_data


# async def get_repo(repo: str):
#     owner, repo = repo.split("/")
#     resp = await github.rest.repos.async_get(owner, repo)
#     return resp.parsed_data
