import os.path
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import List

from workstation import RESOURCES_PATH
from workstation.os_manager import OSManager
from workstation.zsh import ZSH_CONFIG_PATH

PY_SYS = "/usr/bin/python3"
POETRY_HOME = os.path.expanduser("~/.poetry")
PYENV_ROOT = os.path.expanduser("~/.pyenv")
PYENV_ZSH_CONFIG_LOCATION = os.path.join(ZSH_CONFIG_PATH, "pyenv.zsh")
PYENV_ZSH_CONFIG_RESOURCE_LOCATION = os.path.join(RESOURCES_PATH, "zshrc", "pyenv.zsh")
VIRTUALENV_ZSH_CONFIG_LOCATION = os.path.join(ZSH_CONFIG_PATH, "virtualenv.zsh")
VIRTUALENV_ZSH_CONFIG_RESOURCE_LOCATION = os.path.join(
    RESOURCES_PATH, "zshrc", "virtualenv.zsh"
)
POETRY_ZSH_CONFIG_LOCATION = os.path.join(ZSH_CONFIG_PATH, "poetry.zsh")
POETRY_ZSH_CONFIG_RESOURCE_LOCATION = os.path.join(
    RESOURCES_PATH, "zshrc", "poetry.zsh"
)
POETRY_CMD = f"curl -sSL https://install.python-poetry.org | POETRY_HOME={POETRY_HOME} {PY_SYS} -"


@dataclass
class PythonInstaller:
    os_manager: OSManager

    def global_install(self, *args):
        cmd = f"{PY_SYS} -E -m pip install --upgrade " + " ".join(args) + " --user"
        print("********", cmd)
        self.os_manager.run(cmd)

    @staticmethod
    def _remove_pyenv():
        shutil.rmtree(PYENV_ROOT, ignore_errors=True)
        Path(PYENV_ZSH_CONFIG_LOCATION).unlink(missing_ok=True)

    def _install_pyenv(self):
        self.os_manager.native_install(
            "make",
            "gcc",
            "zlib-devel",
            "bzip2",
            "bzip2-devel",
            "readline-devel",
            "sqlite",
            "sqlite-devel",
            "openssl-devel",
            "tk-devel",
            "libffi-devel",
            "xz-devel",
            sudo=True,
        )
        self._remove_pyenv()
        cmd = "curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash"
        self.os_manager.run(cmd)
        shutil.copy(PYENV_ZSH_CONFIG_RESOURCE_LOCATION, PYENV_ZSH_CONFIG_LOCATION)

    def _install_python_versions(self, python_versions: List[str]):
        self.os_manager.run_in_zsh("pyenv update")
        for pv in python_versions:
            cmd = f"pyenv install {pv}"
            self.os_manager.run_in_zsh(cmd)

    def _install_utils(self):
        # TODO: out of the function
        r = ["nox==2021.10.1", "nox-poetry==0.9.0"]
        self.global_install(*r)

    def _install_virtualenv(self):
        r = ["virtualenv==20.10.0", "virtualenvwrapper==4.8.4"]
        self.global_install(*r)
        shutil.copy(
            VIRTUALENV_ZSH_CONFIG_RESOURCE_LOCATION, VIRTUALENV_ZSH_CONFIG_LOCATION
        )

    def _remove_poetry(self):
        Path(POETRY_ZSH_CONFIG_LOCATION).unlink(missing_ok=True)
        cmd = POETRY_CMD + " --uninstall"
        self.os_manager.run(cmd)

    def _install_poetry(self):
        self._remove_poetry()
        cmd = f"curl -sSL https://install.python-poetry.org | POETRY_HOME={POETRY_HOME} {PY_SYS} -"
        self.os_manager.run(cmd)
        shutil.copy(POETRY_ZSH_CONFIG_RESOURCE_LOCATION, POETRY_ZSH_CONFIG_LOCATION)

    def run(self, python_versions: List[str]):
        self._install_pyenv()
        # self._install_python_versions(python_versions=python_versions)
        self._install_virtualenv()
        self._install_poetry()
        self._install_utils()
