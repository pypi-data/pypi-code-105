"""Stream type classes for tap-bexio."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_bexio.client import bexioStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.


class ProjectsStream(bexioStream):
    """Projectsstream."""
    name = "projects"
    path = "pr_project"
    data_key = "project"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "projects.json"


