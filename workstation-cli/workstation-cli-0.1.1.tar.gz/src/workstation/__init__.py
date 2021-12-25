import importlib.resources as pkg_resources
import os

OS_FEDORA = "fedora"
OS_UBUNTU = "ubuntu"
OS_MAC = "macintosh"

HOME = os.environ["HOME"]
RESOURCES_PATH = str(pkg_resources.path("workstation", "resources"))
