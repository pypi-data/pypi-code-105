import os.path
import shutil
import subprocess
import tarfile
from dataclasses import dataclass
from pathlib import Path

import wget

from workstation import HOME
from workstation import OS_FEDORA


def full_path(suffix: str) -> str:
    return os.path.join(HOME, suffix)


@dataclass
class OSManager:
    operating_system: str

    @staticmethod
    def run_in_zsh(cmd):
        pass

    @staticmethod
    def run(cmd) -> int:
        return os.system(cmd)
        # args = shlex.split(cmd)
        # sub = subprocess.Popen(args, stdout=subprocess.PIPE)
        # return sub

    @staticmethod
    def native_update(**kwargs):
        pass

    def native_install(self, *args, **kwargs):
        pass


@dataclass
class Fedora(OSManager):
    operating_system: str = OS_FEDORA

    @staticmethod
    def run_in_zsh(cmd):
        cmd = "source ~/.zshrc;" + cmd
        subprocess.call(cmd, shell=True, executable="/bin/zsh")

    def native_install(self, *args, **kwargs):
        self.native_update(**kwargs)
        cmd = "dnf install -y "
        if kwargs.get("sudo", False):
            cmd = "sudo " + cmd
        cmd += " ".join(args) + " 2>/dev/null"
        os.system(cmd)

    @staticmethod
    def native_update(**kwargs):
        cmd = "dnf update"
        if kwargs.get("sudo", False):
            cmd = "sudo " + cmd
        os.system(cmd)

    @staticmethod
    def tgz_install_from_url(url: str, binary_name: str):
        dest = os.path.expanduser("~/.local/bin")
        os.makedirs(dest, exist_ok=True)
        file = wget.download(url)
        with tarfile.open(file, "r:gz") as tar:
            tar.extractall()
            folder = tar.getnames()[0]
        shutil.copy(os.path.abspath(os.path.join(folder, binary_name)), dest)
        Path(os.path.abspath(file)).unlink(missing_ok=True)
        shutil.rmtree(folder)

    def rpm_install_from_url(self, url: str):
        file = wget.download(url, "tmp.rpm")
        self.native_install("tpm.rpm", sudo=True)
        Path(os.path.abspath(file)).unlink(missing_ok=True)
