from argparse import ArgumentParser

import yaml

from polidoro_install.installer import Installer


def load_yml(packages_file_name):
    with open(packages_file_name, 'r') as packages_file:
        return yaml.load(packages_file, Loader=yaml.FullLoader)


def install_packages():
    parser = ArgumentParser()
    parser.add_argument('packages_to_install', nargs='+')
    parser.add_argument('--packages_file', nargs='?', default='packages.yml')
    parser.add_argument('--force', '-y', action='store_true')
    namespace = parser.parse_args()

    params = dict(namespace.__dict__)
    packages_to_install = params.pop('packages_to_install')
    packages = load_yml(namespace.packages_file)

    installers = {}
    for installer_name, installer_info in packages['installers'].items():
        installers[installer_name] = Installer.create(installer_name, installer_info)

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
    else:
        for i in installers.values():
            if package in i:
                installer = i
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
