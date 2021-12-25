import click
import distro

from workstation.nvm import NVMInstaller
from workstation.os_manager import Fedora
from workstation.python import PythonInstaller
from workstation.sdkman import SDKManInstaller
from workstation.terminal import TilixInstaller
from workstation.zsh import ZSHInstaller


@click.command()
def install_workstation():
    if distro.id() == "fedora":
        os_manager = Fedora()
    else:
        raise ValueError("OS not supported yet!")

    if click.confirm("Do you want to setup Zsh?"):
        zsh_installer = ZSHInstaller(os_manager=os_manager)
        zsh_installer.run()

    if click.confirm("Do you want to install Tilix?"):
        zsh_installer = TilixInstaller(os_manager=os_manager)
        zsh_installer.run()

    if click.confirm("Do you want to setup Python?"):
        python_installer = PythonInstaller(os_manager=os_manager)
        choice = click.prompt(
            "Please select python versions:",
            type=click.Choice(["3.8.12", "3.9.7"]),
            show_default=False,
        )
        python_installer.run(python_versions=[choice])

    if click.confirm("Do you want to setup Node?"):
        nvm_installer = NVMInstaller(os_manager=os_manager)
        choice = click.prompt(
            "Please select node versions:",
            type=click.Choice(["v16.13.0"]),
            show_default=False,
        )
        nvm_installer.run(node_version=choice)

    if click.confirm("Do you want to setup Java?"):
        sdkman_installer = SDKManInstaller(os_manager=os_manager)
        choice = click.prompt(
            "Please select java versions:",
            type=click.Choice(["14.0.2-open"]),
            show_default=False,
        )
        sdkman_installer.run(java_version=choice)
