import copy
from string import Template
from typing import Optional, Dict, List, Union

import os
from pydantic import BaseModel, validator


def _to_list(info: Union[str, List[str]]) -> List[str]:
    return info if isinstance(info, list) else [info]


def replace_environs(cmd):
    resp = []
    for c in _to_list(cmd):
        cmd_aux = None
        while cmd_aux != c:
            cmd_aux = c
            c = Template(c).safe_substitute(**os.environ)
        resp.append(c)
    return resp


class Installer(BaseModel):
    pre_install: Optional[List[str]] = []
    command: Union[List[str], str]
    post_install: Optional[List[str]] = []
    packages: Optional[Dict] = {}
    force: bool = False
    check_installation: Optional[str]
    packages_to_install: Optional[List[str]] = []
    requires: Optional[List[str]] = []
    name: str
    environment: Optional[Dict] = {}
    can_force: bool = False
    solo_package: bool = False

    # validators
    _to_list_pre_install = validator('pre_install', allow_reuse=True, pre=True)(_to_list)
    _to_list_post_install = validator('post_install', allow_reuse=True, pre=True)(_to_list)
    _to_list_requires = validator('requires', allow_reuse=True, pre=True)(_to_list)
    _to_list_command = validator('command', allow_reuse=True, pre=True)(_to_list)

    @validator('packages')
    def validate_packages(cls, packages):
        packs = {}
        for name, info in packages.items():
            info.setdefault('package', name)
            if isinstance(info, str):
                info = dict(package=info)
            packs[name] = Package(**info, name=name)
        return packs

    def install(self, packages=None):
        packages = packages or []
        packages.extend(self.packages_to_install)
        if not packages:
            return

        pre_packages = []
        pos_packages = []
        packages_to_install = []
        repo_keys = []
        repo_entries = []
        original_environ = copy.deepcopy(os.environ)
        os.environ.update(self.environment)
        for package in packages:
            if not self.already_installed(package):
                pre_packages += _to_list(package.pre_install) if package.pre_install is not None else []
                pos_packages += _to_list(package.post_install) if package.post_install is not None else []
                packages_to_install.append(package.package)
                os.environ.update(package.environment)
                if package.repo_key:
                    repo_keys.append(f'wget -qO - {package.repo_key} | sudo apt-key add -')
                if package.repo_entry:
                    repo_entries.append(
                        f'echo "{package.repo_entry}" | sudo tee /etc/apt/sources.list.d/{package.package}.list'
                    )

        if packages_to_install:
            Installer.exec(pre_packages)
            Installer.exec(repo_keys)
            Installer.exec(repo_entries)
            Installer.exec(self.pre_install)
            Installer.exec(self.install_command(packages_to_install))
            Installer.exec(pos_packages)
            Installer.exec(self.post_install)
        else:
            print('The packages "%s" %s already installed' %
                  ('", "'.join([p.name for p in packages]), 'is' if len(packages) == 1 else 'are'))
        self.clear_install_list()
        os.environ = original_environ

    def add_to_install(self, package):
        self.packages_to_install.append(package)

    def clear_install_list(self):
        self.packages_to_install = []

    def already_installed(self, package):
        if not self.check_installation:
            return False

        if not self.packages:
            check_installation_cmd = self.check_installation
        elif '$package' in self.check_installation:
            check_installation_cmd = Template(self.check_installation).safe_substitute(package=package.package)
        else:
            check_installation_cmd = f'{self.check_installation} {package.package}'

        if self.check_installation.startswith('exists'):
            locals().update(exists=lambda path: os.path.exists(os.path.expanduser(path)))
            check_installation_cmd = replace_environs(check_installation_cmd)
            for ci_cmd in check_installation_cmd:
                if not eval(ci_cmd):
                    return False
            return True

        return not Installer.exec(
            f'{check_installation_cmd} > /dev/null 2>&1',
            print_cmd=False,
            exit_if_error=False)

    def get_requires(self, package):
        if not isinstance(package, Package):
            package = self[package]
        return self.requires + package.requires

    def install_command(self, packages_to_install):
        final_command = self.command
        if self.can_force and self.force:
            final_command = [' '.join(final_command + ['-y'])]
        if not self.solo_package:
            if any('$package' in c for c in final_command):
                new_final_command = []
                for fc in final_command:
                    if '$package' in fc:
                        new_final_command.extend([Template(fc).safe_substitute(package=p) for p in packages_to_install])
                    else:
                        new_final_command.append(fc)
                final_command = new_final_command
            else:
                final_command = [' '.join(final_command + packages_to_install)]
        return final_command

    def add_package(self, package):
        dict_item = dict(package=package, name=package)
        self.packages[package] = Package(**dict_item, installer=self)

    @staticmethod
    def exec(cmd, print_cmd=True, exit_if_error=True):
        for c in replace_environs(cmd):
            if print_cmd:
                print(f'+ {c}')

            if c.lower().startswith('cd'):
                os.chdir(os.path.expanduser(c[2:].strip()))
                continue

            error = os.system(c)
            if error:
                if exit_if_error:
                    exit(error)
                return error

        return 0

    @staticmethod
    def create(name, **info):
        installer = Installer(**info, name=name)
        for package in installer.packages.values():
            package.installer = installer
        return installer

    def __getitem__(self, item):
        return self.packages[item]

    def __contains__(self, item):
        return item in self.packages


class Package(BaseModel):
    pre_install: Optional[List[str]] = []
    package: str
    post_install: Optional[List[str]] = []
    requires: Optional[List[str]] = []
    installer: Optional[Installer]
    name: str
    environment: Optional[Dict] = {}
    repo_key: Optional[str] = ''
    repo_entry: Optional[str] = ''

    _to_list_pre_install = validator('pre_install', allow_reuse=True, pre=True)(_to_list)
    _to_list_post_install = validator('post_install', allow_reuse=True, pre=True)(_to_list)
    _to_list_requires = validator('requires', allow_reuse=True, pre=True)(_to_list)

    def __hash__(self):
        return hash(self.package)

    def __eq__(self, other):
        if isinstance(other, Package):
            other = other.package
        return other == self.package

    def __str__(self):
        return self.package

    def __repr__(self):
        return str(self)

    def add_to_install(self):
        self.installer.add_to_install(self)
