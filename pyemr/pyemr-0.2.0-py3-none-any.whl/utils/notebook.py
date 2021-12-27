""" """
import json
import os
import sys
from pprint import pprint

from ipykernel.kernelspec import install
from jupyter_client.kernelspec import KernelSpecManager

from pyemr.utils.sys import get_site_package_paths


def install_mock_python_kernal(site_packages: str):
    """

    Args:
      site_packages: str:
      site_packages: str:

    Returns:

    """

    print("install_mock_python_kernal.site_packages", site_packages)
    # site_packages :str :
    kernal_path = install(
        user=True,
        kernel_name="pyemr",
        display_name="PYEMR (s3-mock)",
    )
    print("kernal_path", kernal_path)
    with open(f"{kernal_path}/kernel.json") as f:
        kernal = json.load(f)

    for i, arg in enumerate(kernal["argv"]):
        if "ipykernel_launcher" == arg:
            break
    else:
        raise ValueError("Something went wrong. No 'ipykernel_launcher' arg found in Kernel config.")

    kernal["argv"] = (
        kernal["argv"][:i]
        + ["pyemr.utils.ipykernel_launcher", site_packages]
        + kernal["argv"][i + 1 :]
    )

    with open(f"{kernal_path}/kernel.json", "w") as f:
        json.dump(kernal, f)
    
    pprint(list_jupyter_kernels())



def run_notebook_on_sys(site_packages=""):
    """

    Args:
      site_packages: (Default value = '')

    Returns:

    """
    print("site_packages", site_packages)
    site_packages = ",".join([site_packages] + get_site_package_paths())
    install_mock_python_kernal(site_packages)
    os.system("jupyter notebook --ip 0.0.0.0 --no-browser --allow-root --port 8889")


def run_notebook_in_poetry():
    """ """

    site_packages = ",".join(get_site_package_paths())

    if not os.path.exists("pyproject.toml"):
        raise ValueError("No pyproject.toml exists. Run 'pyemr init'")

    os.system("poetry install")

    from pyemr.utils.poetry import install_pyemr_in_poetry_env

    install_pyemr_in_poetry_env()

    print(f"poetry run python -m pyemr.utils.notebook sys {site_packages}")
    os.system(f"poetry run python -m pyemr.utils.notebook sys {site_packages}")


def launch_mock_notebook_docker():
    """Launch an interactive python session from inside docker. With mock s3.

    Args:
      *args:
      **kwards:

    Returns:

    """
    # args = " ".join(args)
    # kwards = " ".join(["-{k} {v}" for k, v in kwards.items()])
    from pyemr.utils.docker import docker_build_run

    docker_build_run("/pyemr/sh/run_notebook.sh")


def list_jupyter_kernels():
    """ """
    return KernelSpecManager().get_all_specs()


if __name__ == "__main__":

    if sys.argv[1] in ["os", "local", "sys"]:
        site_packages = sys.argv[2] if len(sys.argv) == 3 else ""
        run_notebook_on_sys(site_packages)

    if sys.argv[1] in ["poetry", "venv"]:
        run_notebook_in_poetry()

    if sys.argv[1] in ["docker", "linux"]:
        launch_mock_notebook_docker()
