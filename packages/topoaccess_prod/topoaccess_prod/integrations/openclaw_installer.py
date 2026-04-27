from ..install.harness_installer import install_target


def install(profile: str = "default", dry_run: bool = True) -> dict:
    return install_target("openclaw", profile, dry_run)
