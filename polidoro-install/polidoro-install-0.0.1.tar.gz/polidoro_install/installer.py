from typing import Optional, Dict, List, Union

import os
from pydantic import BaseModel, validator


def _to_list(info: Union[str, List[str]]) -> List[str]:
    return info if isinstance(info, list) else [info]


class Installer(BaseModel):
    pre_install: Optional[List[str]] = []
    command: str
    pos_install: Optional[List[str]] = []
    packages: Optional[Dict] = {}
    force: bool = False
    check_installation: Optional[str]
    packages_to_install: Optional[List[str]] = []
    requires: Optional[List[str]] = []
    name: str

    # validators
    _to_list_pre_install = validator('pre_install', allow_reuse=True, pre=True)(_to_list)
    _to_list_pos_install = validator('pos_install', allow_reuse=True, pre=True)(_to_list)
    _to_list_requires = validator('requires', allow_reuse=True, pre=True)(_to_list)

    @validator('packages')
    def validate_packages(cls, packages):
        packs = {}
        for name, info in packages.items():
            info.setdefault('package', name)
            if isinstance(info, str):
                info = dict(package=info)
            packs[name] = Package(**info, name=name)
        return packs

    def install(self, packages=None, show_already_installed_message=True):
        if self.requires:
            pass
        packages = packages or []
        packages.extend(self.packages_to_install)
        if not packages:
            return
        pre_packages = []
        pos_packages = []
        packages_to_install = []
        for p in packages:
            pre, package_to_install, pos = self.get_install_info(self[p])
            pre_packages.extend(pre)
            if package_to_install:
                packages_to_install.append(package_to_install)
            pos_packages.extend(pos)

        if packages_to_install:
            Installer.exec(pre_packages)
            Installer.exec(self.pre_install)
            Installer.exec(f'{self.command} {" ".join(packages_to_install)}' + (' -y' if self.force else ''))
            Installer.exec(pos_packages)
            Installer.exec(self.pos_install)
        elif show_already_installed_message:
            print(f'The packages "{" ".join([p.name for p in packages])}" are already installed')
        self.clear_install_list()

    def add_to_install(self, package):
        package = self[package]
        self.packages_to_install.append(package)

    def clear_install_list(self):
        self.packages_to_install = []

    def get_install_info(self, package):
        if Installer.exec(
                f'{self.check_installation} {package.package} > /dev/null 2>&1',
                print_cmd=False,
                exit_if_error=False):
            pre_packages = _to_list(package.pre_install) if package.pre_install is not None else []
            pos_packages = _to_list(package.pos_install) if package.pos_install is not None else []
            return pre_packages, package.package, pos_packages
        return [], None, []

    def get_requires(self, package):
        if not isinstance(package, Package):
            package = self[package]
        return self.requires + package.requires

    @staticmethod
    def exec(cmd, print_cmd=True, exit_if_error=True):
        if isinstance(cmd, list):
            for c in cmd:
                error = Installer.exec(c, print_cmd=print_cmd, exit_if_error=exit_if_error)
                if error:
                    return error

            return 0
        error = 1
        if cmd:
            if print_cmd:
                print(f'+ {cmd}')

            error = os.system(cmd)
            if error and exit_if_error:
                exit(error)

        return error

    @staticmethod
    def create(name, info):
        installer = Installer(**info, name=name)
        for package in installer.packages.values():
            package.installer = installer
        return installer

    def __getitem__(self, item):
        if isinstance(item, Package):
            return item
        dict_item = dict(package=item, name=item)
        return self.packages.get(item, Package(**dict_item, installer=self))

    def __contains__(self, item):
        return item in self.packages


class Package(BaseModel):
    pre_install: Optional[List[str]] = []
    package: str
    pos_install: Optional[List[str]] = []
    requires: Optional[List[str]] = []
    installer: Optional[Installer]
    name: str

    _to_list_pre_install = validator('pre_install', allow_reuse=True, pre=True)(_to_list)
    _to_list_pos_install = validator('pos_install', allow_reuse=True, pre=True)(_to_list)
    _to_list_requires = validator('requires', allow_reuse=True, pre=True)(_to_list)

    def __hash__(self):
        return hash(self.package)

    def __eq__(self, other):
        if isinstance(other, Package):
            other = other.package
        return other == self.package

    def add_to_install(self):
        self.installer.add_to_install(self)
