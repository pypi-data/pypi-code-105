import os.path
import shutil
from dataclasses import dataclass
from pathlib import Path

from workstation import RESOURCES_PATH
from workstation.os_manager import OSManager
from workstation.zsh import ZSH_CONFIG_PATH

SDKMAN_ROOT = os.path.expanduser("~/.sdkman")
SDKMAN_ZSH_CONFIG_LOCATION = os.path.join(ZSH_CONFIG_PATH, "sdkman.zsh")
SDKMAN_ZSH_CONFIG_RESOURCE_LOCATION = os.path.join(
    RESOURCES_PATH, "zshrc", "sdkman.zsh"
)


@dataclass
class SDKManInstaller:
    os_manager: OSManager

    @staticmethod
    def _remove_sdkman():
        shutil.rmtree(SDKMAN_ROOT, ignore_errors=True)

    def _install_sdkman(self):
        self._remove_sdkman()
        cmd = f'export SDKMAN_DIR="{SDKMAN_ROOT}" && curl -s "https://get.sdkman.io?rcupdate=false" | bash'
        self.os_manager.run(cmd)

    def _install_java(self, java_version: str):
        cmds = [
            "sdk install maven",
            f"sdk install java {java_version}",
            f"sdk default java {java_version}",
        ]
        for cmd in cmds:
            self.os_manager.run_in_zsh(cmd)

    @staticmethod
    def _remove_sdkman_zsh_config():
        Path(SDKMAN_ZSH_CONFIG_LOCATION).unlink(missing_ok=True)

    def _setup_sdkman_zsh_config(self):
        self._remove_sdkman_zsh_config()
        shutil.copy(SDKMAN_ZSH_CONFIG_RESOURCE_LOCATION, SDKMAN_ZSH_CONFIG_LOCATION)

    def run(self, java_version: str):
        self._install_sdkman()
        self._setup_sdkman_zsh_config()
        self._install_java(java_version=java_version)
