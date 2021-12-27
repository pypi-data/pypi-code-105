""" """
import os
import sys


def launch_mock_python():
    """ """
    from pyemr.utils.mocking import launch_python_mock_on_sys

    launch_python_mock_on_sys()


def launch_mock_python_inherit_site_packages(site_packages):
    """

    Args:
      site_packages:

    Returns:

    """

    for path in site_packages:
        if path not in sys.path:
            sys.path.append(path)

    from pyemr.utils.mocking import launch_python_mock_on_sys

    launch_python_mock_on_sys()


def launch_mock_python_venv():
    """ """
    from pyemr.utils.poetry import install_pyemr_in_poetry_env

    spks = []
    for path in sys.path:
        if path.endswith("site-packages"):
            if path not in spks:
                spks.append(path)

    if not os.path.exists("pyproject.toml"):
        raise ValueError("No pyproject.toml exists. Run 'pyemr init'")

    os.system("poetry install")
    install_pyemr_in_poetry_env()
    cmd = [
        "poetry",
        "run",
        "python",
        "-c",
        '"from',
        "pyemr.utils.python",
        "import",
        "launch_mock_python_inherit_site_packages;",
        f'launch_mock_python_inherit_site_packages({spks})"',
    ]
    os.system(" ".join(cmd))


def launch_mock_python_docker():
    """Launch an interactive python session from inside docker. With mock s3.

    Args:
      *args:
      **kwards:

    Returns:

    """
    # args = " ".join(args)
    # kwards = " ".join(["-{k} {v}" for k, v in kwards.items()])
    from pyemr.utils.docker import docker_build_run

    docker_build_run("/pyemr/sh/run_pyemr_python_mock.sh")


if __name__ == "__main__":

    if sys.argv[1] in ["os", "local", "sys"]:
        launch_mock_python()

    if sys.argv[1] in ["poetry", "venv"]:
        launch_mock_python_venv()

    if sys.argv[1] in ["docker"]:
        launch_mock_python_docker()
