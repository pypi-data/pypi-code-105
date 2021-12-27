""" """
import os
import shutil
import sys


def get_site_package_paths():
    """ """

    spks = []
    for path in sys.path:
        if path.endswith("site-packages"):
            if path not in spks:
                spks.append(path)

    return spks


def copy_and_overwrite(from_path, to_path):
    """

    Args:
      from_path:
      to_path:

    Returns:

    """
    if os.path.exists(to_path):
        shutil.rmtree(to_path)

    # os.makedirs(to_path, exist_ok=True)
    shutil.copytree(from_path, to_path)
