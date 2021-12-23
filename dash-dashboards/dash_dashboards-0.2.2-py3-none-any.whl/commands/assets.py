import shutil
from pathlib import Path

import click

from .config import DEFAULT_ASSETS_DIR

_ASSETS_SRC_DIR = (
    Path(__file__).parent.parent.resolve() / DEFAULT_ASSETS_DIR
).resolve()


def generate_assets(assets_dest_dir: Path):
    shutil.copytree(_ASSETS_SRC_DIR, assets_dest_dir, dirs_exist_ok=True)


@click.command(name="generate-assets")
@click.option(
    "-d",
    "--assets-dir",
    prompt="Assets directory",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path(DEFAULT_ASSETS_DIR),
    help="Path to the dashboards directory",
)
def generate_assets_cmd(assets_dir: Path):
    if assets_dir.exists():
        new_assets = [
            f.relative_to(_ASSETS_SRC_DIR)
            for f in _ASSETS_SRC_DIR.rglob("*")
            if f.is_file()
        ]

        assets_overwrite = [
            f
            for f in assets_dir.rglob("*")
            if f.is_file() and f.relative_to(assets_dir) in new_assets
        ]

        file_list = "\n".join([f"  * {f}" for f in assets_overwrite])
        msg = (
            "This command will overwrite all changes you made in the "
            f"following files:\n{file_list}"
            "\nDo you want to continue?"
        )
        click.confirm(msg, abort=True)
    generate_assets(assets_dir)
