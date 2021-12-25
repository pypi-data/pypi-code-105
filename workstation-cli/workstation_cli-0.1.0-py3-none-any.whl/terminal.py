import os.path
import shutil
from dataclasses import dataclass

from workstation import RESOURCES_PATH
from workstation.os_manager import full_path
from workstation.os_manager import OSManager

DCONF_LOCATION = os.path.join(RESOURCES_PATH, "tilix.dconf")


@dataclass
class TilixInstaller:
    os_manager: OSManager

    def _install_tilix(self):
        self.os_manager.native_install("tilix", sudo=True)

    def _install_custom_theme(self):
        self.os_manager.run(f"dconf load /com/gexperts/Tilix/ <{DCONF_LOCATION}")
        shutil.rmtree(
            os.path.expanduser("~/.local/share/fonts-tmp"), ignore_errors=True
        )
        os.system(
            f"git clone https://github.com/romkatv/powerlevel10k-media.git {full_path('.local/share/fonts-tmp/')}"
        )
        os.makedirs(os.path.expanduser("~/.local/share/fonts"), exist_ok=True)
        files = os.listdir(os.path.expanduser("~/.local/share/fonts-tmp/"))
        for x in files:
            if x.startswith("Meslo"):
                shutil.copyfile(
                    os.path.join(os.path.expanduser("~/.local/share/fonts-tmp/"), x),
                    os.path.join(os.path.expanduser("~/.local/share/fonts"), x),
                )
        shutil.rmtree(
            os.path.expanduser("~/.local/share/fonts-tmp"), ignore_errors=True
        )

    def run(self):
        self._install_tilix()
        self._install_custom_theme()
