from dataclasses import dataclass

import requests

from workstation import OS_FEDORA
from workstation.os_manager import Fedora
from workstation.os_manager import OSManager


@dataclass
class MiscellaneousInstaller:
    os_manager: OSManager

    def _install_jetbrains_toolbox(self):
        if self.os_manager.operating_system == OS_FEDORA:
            os_manager: Fedora = self.os_manager
            r = requests.get(
                "https://data.services.jetbrains.com//products/releases?code=TBA&latest=true&type=release"
            )
            url = r.json()["TBA"][0]["downloads"]["linux"]["link"]
            os_manager.tgz_install_from_url(url, "jetbrains-toolbox")

    def run(self):
        self._install_jetbrains_toolbox()
