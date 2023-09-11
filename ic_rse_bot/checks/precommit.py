from ic_rse_bot.repo import Repository

# def raw_url(repo: str, path: str) -> str:
#     return f"https://raw.githubusercontent.com/{repo}/HEAD/{path}"


async def run_check(repo: Repository) -> str | None:
    # async with github.get_async_client() as client:
    #     resp = await client.get(raw_url(repo, item.path))
    #     resp.raise_for_status()

    #     print(resp.content)
    #     config = yaml.safe_load(resp.content)
    #     print(config)
    if ".pre-commit-config.yaml" not in repo.files:
        return "You should consider using pre-commit"

    return None
