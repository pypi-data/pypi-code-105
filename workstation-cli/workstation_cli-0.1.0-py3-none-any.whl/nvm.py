import os.path
import shutil
from dataclasses import dataclass
from pathlib import Path

from workstation import RESOURCES_PATH
from workstation.os_manager import OSManager
from workstation.zsh import ZSH_CONFIG_PATH

NVM_ROOT = os.path.expanduser("~/.nvm")
NVM_ZSH_CONFIG_LOCATION = os.path.join(ZSH_CONFIG_PATH, "nvm.zsh")
NVM_ZSH_CONFIG_RESOURCE_LOCATION = os.path.join(RESOURCES_PATH, "zshrc", "nvm.zsh")


@dataclass
class NVMInstaller:
    os_manager: OSManager

    @staticmethod
    def _remove_nvm():
        shutil.rmtree(NVM_ROOT, ignore_errors=True)

    def _install_nvm(self):
        self._remove_nvm()
        cmd = f"git clone https://github.com/nvm-sh/nvm.git {NVM_ROOT}"
        self.os_manager.run(cmd)

    def _install_node(self, node_version: str):
        cmd = f"nvm install {node_version}"
        self.os_manager.run_in_zsh(cmd)

    @staticmethod
    def _remove_nvm_zsh_config():
        Path(NVM_ZSH_CONFIG_LOCATION).unlink(missing_ok=True)

    def _setup_nvm_zsh_config(self):
        self._remove_nvm_zsh_config()
        shutil.copy(NVM_ZSH_CONFIG_RESOURCE_LOCATION, NVM_ZSH_CONFIG_LOCATION)

    def run(self, node_version: str):
        self._install_nvm()
        self._setup_nvm_zsh_config()
        self._install_node(node_version=node_version)
