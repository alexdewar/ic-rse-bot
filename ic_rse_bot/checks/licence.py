from ic_rse_bot.checks import BaseCheck
from ic_rse_bot.repo import Repository

_NO_LICENCE = (
    "No licence file was found in your repository. You should consider "
    "adding a licence so that users know what they are and are not permitted to do "
    "with your source code.\n\n"
    "For more information, see [Imperial College's advice about making your research "
    "software available](https://www.imperial.ac.uk/research-and-innovation/support-for-staff/scholarly-communication/research-data-management/sharing-data/research-software/)."  # noqa: E501
)


class LicenceCheck(BaseCheck):
    def __init__(self) -> None:
        super().__init__("Licence", "Add a licence file")

    async def run(self, repo: Repository) -> str | None:
        if not repo.license_:
            return _NO_LICENCE

        return None
