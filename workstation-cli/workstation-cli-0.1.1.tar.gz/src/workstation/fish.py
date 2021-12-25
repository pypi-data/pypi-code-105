# import importlib.resources as pkg_resources
# import os
# import shutil
# from dataclasses import dataclass
# from pathlib import Path
#
# from loguru import logger
#
# from workstation.utils import full_path, OSManager
#
# fishRC_PATH = os.path.expanduser("~/.fishrc")
# fish_CONFIG_PATH = os.path.expanduser("~/.configs")
# OH_MY_FISH_PATH = os.path.expanduser("~/.oh-my-fish")
#
# RESOURCES_PATH = str(pkg_resources.path("workstation", "resources"))
#
#
# @dataclass
# class FishInstaller:
#     os_manager: OSManager
#
#     def install_fish(self):
#         logger.info("Installing fish")
#         self.os_manager.native_install("fish", sudo=True)
#
#     def install_oh_my_fish(self):
#         logger.info("Installing oh-my-fish")
#         shutil.rmtree(OH_MY_fish_PATH, ignore_errors=True)
#         cmd = 'sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyfish/ohmyfish/master/tools/install.sh)" "" ' \
#               '--unattended '
#         self.os_manager.run(cmd)
#
#     def install_fish_plugins(self):
#         logger.info("Installing fish plugins")
#         cmds = [
#             "git clone https://github.com/fish-users/fish-syntax-highlighting.git ${"
#             "fish_CUSTOM:-~/.oh-my-fish/custom}/plugins/fish-syntax-highlighting",
#             "git clone https://github.com/fish-users/fish-autosuggestions ${"
#             "fish_CUSTOM:-~/.oh-my-fish/custom}/plugins/fish-autosuggestions",
#             "git clone https://github.com/fish-users/fish-completions ${"
#             "fish_CUSTOM:=~/.oh-my-fish/custom}/plugins/fish-completions "
#         ]
#         for cmd in cmds:
#             self.os_manager.run(cmd)
#
#     @staticmethod
#     def setup_fish_config():
#         logger.info("Setup fish")
#         Path(fishRC_PATH).unlink(missing_ok=True)
#         fishrc_location = os.path.join(RESOURCES_PATH, ".fishrc")
#         shutil.copy(fishrc_location, fishRC_PATH)
#         shutil.rmtree(fish_CONFIG_PATH, ignore_errors=True)
#         fish_config_location = os.path.join(RESOURCES_PATH, "fishrc")
#         shutil.copytree(fish_config_location, os.path.join(fish_CONFIG_PATH, "fishrc"), dirs_exist_ok=True)
#
#     def install_theme(self):
#         logger.info("Setup fish theme")
#         cmd = f"git clone --depth=1 https://github.com/romkatv/powerlevel10k.git {OH_MY_fish_PATH}/custom/themes" \
#               f"/powerlevel10k"
#         self.os_manager.run(cmd)
#         p10k_location = os.path.join(RESOURCES_PATH, ".p10k.fish")
#         shutil.copy(p10k_location, os.path.expanduser("~/.p10k.fish"))
#
#     def change_shell(self):
#         logger.info("Changing default shell to fish")
#         self.os_manager.run("chsh -s /usr/bin/fish")
#
#     def run_full_setup(self):
#         try:
#             self.install_fish()
#             self.install_fish_plugins()
#             self.install_oh_my_fish()
#             self.install_theme()
#             self.setup_fish_config()
#         except KeyboardInterrupt:
#             logger.info("\n\n\033[0;31m❌ Aborting setup!\033[0m")
#
#
