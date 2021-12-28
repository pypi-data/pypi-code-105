import os.path
import re
from argparse import ArgumentParser

import requests
import yaml

from polidoro_install.installer import Installer

CONFIG_PATH = os.path.expanduser('~/.pinstall')
if not os.path.exists(CONFIG_PATH):
    os.mkdir(CONFIG_PATH)


def default_packages_file():
    from polidoro_install import VERSION
    return f'{CONFIG_PATH}/packages-{VERSION}.yml'


def load_yml(packages_file_name):
    try:
        with open(packages_file_name, 'r') as packages_file:
            return yaml.safe_load(packages_file)
    except FileNotFoundError:
        if packages_file_name == default_packages_file():
            os.chdir(CONFIG_PATH)
            for file in os.listdir():
                if file.endswith('.bkp'):
                    print(f'Removing file: {file}')
                    os.remove(file)
                elif re.match(r'packages-\d*.\d*.\d*.yml', file):
                    print(f'Renaming file: {file} to {file}.bkp')
                    os.rename(file, f'{file}.bkp')
            print('Downloading updated packages file...')
            open(default_packages_file(), 'wb').write(
                requests.get(
                    'https://raw.githubusercontent.com/heitorpolidoro/polidoro-install/master/packages.yml'
                ).content)
            with open(packages_file_name, 'r') as packages_file:
                return yaml.safe_load(packages_file)


def install_packages():
    parser = ArgumentParser()
    parser.add_argument('packages_to_install', nargs='*')
    parser.add_argument('--packages_file', nargs='?', default=default_packages_file())
    parser.add_argument('--install_file', nargs='?')
    parser.add_argument('--force', '-y', action='store_true')
    namespace = parser.parse_args()

    params = dict(namespace.__dict__)
    packages_to_install = params.pop('packages_to_install')
    if namespace.install_file:
        with open(namespace.install_file, 'r') as file:
            packages_to_install.extend([p for p in file.read().split('\n') if p and not p.startswith('#')])
    packages = load_yml(namespace.packages_file)

    installers = {}
    for installer_name, installer_info in packages['installers'].items():
        installers[installer_name] = Installer.create(installer_name, **installer_info, **params)

    requires_map = {}
    while packages_to_install:
        package = packages_to_install.pop()
        package = get_package(installers, package)

        requires = package.installer.get_requires(package)

        requires_map[package] = set(requires)
        packages_to_install.extend(requires)

    installation_order = []
    while requires_map:
        without_dependencies = [package for package, requires in requires_map.items() if not requires]
        for package in without_dependencies:
            requires_map.pop(package)
            for dependencies in requires_map.values():
                dependencies.discard(package.package)
                dependencies.discard(f'{package.installer.name}:{package.package}')
        installation_order.append(without_dependencies)

    for package_list in installation_order:
        show_already_installed_message = package_list == installation_order[-1]
        for package in package_list:
            package.add_to_install()
        for installer in installers.values():
            installer.install(show_already_installed_message=show_already_installed_message)


def get_package(installers, package):
    installer = None
    if ':' in package:
        installer_name, _, package = package.partition(':')
        installer = installers[installer_name]
        installer.add_package(package)

    else:
        for installer_name, installer_info in installers.items():
            if package == installer_name or package in installer_info:
                installer = installer_info
                if package == installer_name:
                    installer.add_package(package)
                    installer.solo_package = True
                break
    if not installer:
        raise ValueError(f'Installer for package "{package}" not found')
    return installer[package]


def main():
    try:
        install_packages()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
