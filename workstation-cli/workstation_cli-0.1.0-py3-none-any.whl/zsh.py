import os
import shutil
from dataclasses import dataclass
from pathlib import Path

from loguru import logger

from workstation import RESOURCES_PATH
from workstation.os_manager import OSManager

ZSHRC_PATH = os.path.expanduser("~/.zshrc")
ZSH_CONFIG_PATH = os.path.expanduser("~/.config/zsh/config.d")
OH_MY_ZSH_PATH = os.path.expanduser("~/.oh-my-zsh")


@dataclass
class ZSHInstaller:
    os_manager: OSManager

    def _install_zsh(self):
        logger.info("Installing zsh")
        self.os_manager.native_install("zsh fd-find", sudo=True)

    def _install_oh_my_zsh(self):
        logger.info("Installing oh-my-zsh")
        shutil.rmtree(OH_MY_ZSH_PATH, ignore_errors=True)
        cmd = (
            'sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" '
            "--unattended "
        )
        self.os_manager.run(cmd)

    def _install_oh_my_zsh_plugins(self):
        logger.info("Installing zsh plugins")
        cmds = [
            "git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${"
            "ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting",
            "git clone https://github.com/zsh-users/zsh-autosuggestions ${"
            "ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions",
            "git clone https://github.com/zsh-users/zsh-completions ${"
            "ZSH_CUSTOM:=~/.oh-my-zsh/custom}/plugins/zsh-completions ",
        ]
        for cmd in cmds:
            self.os_manager.run(cmd)

    @staticmethod
    def _setup_zsh_config():
        logger.info("Setup zsh")
        Path(ZSHRC_PATH).unlink(missing_ok=True)
        zshrc_location = os.path.join(RESOURCES_PATH, ".zshrc")
        shutil.copy(zshrc_location, ZSHRC_PATH)
        for conf in ["banner.zsh", "init.zsh"]:
            os.makedirs(ZSH_CONFIG_PATH, exist_ok=True)
            resource_path = os.path.join(RESOURCES_PATH, "zshrc", conf)
            local_path = os.path.join(ZSH_CONFIG_PATH, conf)
            Path(local_path).unlink(missing_ok=True)
            shutil.copy(resource_path, local_path)

    def _install_theme(self):
        logger.info("Setup zsh theme")
        cmd = (
            f"git clone --depth=1 https://github.com/romkatv/powerlevel10k.git {OH_MY_ZSH_PATH}/custom/themes"
            f"/powerlevel10k"
        )
        self.os_manager.run(cmd)
        p10k_location = os.path.join(RESOURCES_PATH, ".p10k.zsh")
        shutil.copy(p10k_location, os.path.expanduser("~/.p10k.zsh"))

    def _change_shell(self):
        logger.info("Changing default shell to zsh")
        self.os_manager.run("chsh -s /usr/bin/zsh")

    def run(self):
        try:
            self._install_zsh()
            self._install_oh_my_zsh()
            self._install_oh_my_zsh_plugins()
            self._install_theme()
            self._setup_zsh_config()
            self._change_shell()
        except KeyboardInterrupt:
            logger.info("\n\n\033[0;31m❌ Aborting setup!\033[0m")
