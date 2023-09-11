# import yaml

from .repo import get_tree


def raw_url(repo: str, path: str) -> str:
    return f"https://raw.githubusercontent.com/{repo}/HEAD/{path}"


async def check_precommit(repo: str) -> bool:
    tree = await get_tree(repo, "HEAD")
    for item in tree.tree:
        if item.path == ".pre-commit-config.yaml":
            # async with github.get_async_client() as client:
            #     resp = await client.get(raw_url(repo, item.path))
            #     resp.raise_for_status()

            #     print(resp.content)
            #     config = yaml.safe_load(resp.content)
            #     print(config)

            return True

    return False


async def run_checks(repo: str) -> None:
    has_precommit = await check_precommit(repo)
    if has_precommit:
        print(f"{repo} using pre-commit")
    else:
        print(f"{repo} not using pre-commit")
