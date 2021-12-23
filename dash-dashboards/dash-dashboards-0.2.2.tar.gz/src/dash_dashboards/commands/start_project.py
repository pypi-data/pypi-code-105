from pathlib import Path

import click

from .assets import generate_assets
from .config import (
    DEFAULT_ASSETS_DIR,
    DEFAULT_DASHBOARDS_DIR,
    DEFAULT_RUNSERVER_FILE,
    DEFAULT_SETTINGS_FILE,
)
from .utils import valid_dir_name, validate_path_does_not_exist

SETTINGS_CONTENT = """import pathlib

from dash_dashboards.app import DashboardApp, MenuGroup, MenuItem

ASSETS_DIR = (pathlib.Path(__file__).parent / "assets").resolve()

app = DashboardApp(
    title="{project_name}",
    menu=[],
    assets_folder=ASSETS_DIR,
)
"""

RUNSERVER_CONTENT = """from dash_dashboards.commands import run_server

from settings import app

run_server(obj=app)
"""

WSGI_CONTENT = """# !pip install -r requirements.txt

import os

from settings import app

app.run_server(port=int(os.environ["CDSW_READONLY_PORT"]))
"""


@click.command(name="startproject")
@click.option("-n", "--name", prompt="Project name", type=str, help="Project name.")
@click.option(
    "-p",
    "--dir-path",
    prompt="Directory path",
    type=click.Path(exists=True, file_okay=False, resolve_path=True, path_type=Path),
    default=Path("./").resolve(),
    help="Path to the directory where project will be created.",
)
def start_project(name: str, dir_path: Path):
    project_dir_name = valid_dir_name(name)
    project_path = dir_path / project_dir_name

    validate_path_does_not_exist(project_path)
    project_path.mkdir()

    settings_path = project_path / DEFAULT_SETTINGS_FILE
    runserver_file = project_path / DEFAULT_RUNSERVER_FILE
    dashboards_path = project_path / DEFAULT_DASHBOARDS_DIR
    wsgi_file = project_path / "wsgi.py"
    assets_path = project_path / DEFAULT_ASSETS_DIR

    dashboards_path.mkdir()
    with settings_path.open("w") as fp:
        fp.writelines(SETTINGS_CONTENT.format(project_name=name))

    with runserver_file.open("w") as fp:
        fp.writelines(RUNSERVER_CONTENT)

    with wsgi_file.open("w") as fp:
        fp.writelines(WSGI_CONTENT)

    generate_assets(assets_path)
