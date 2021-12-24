
import importlib
import pkgutil
from argparse import ArgumentParser

_CONTEXT = {}


def main():
    parser = ArgumentParser(prog='kpc')
    discovered_plugins = {
        name: importlib.import_module(name)
        for finder, name, ispkg in pkgutil.iter_modules() if name.startswith('kpc_')
    }
    subparsers = parser.add_subparsers(
        title='Commands', description='Valid commands from installed plugins.', help='description')
    for n, m in discovered_plugins.items():
        _CONTEXT[m.PLUGIN_NAME] = m.init_plugin(
            subparsers.add_parser(m.PLUGIN_NAME, description=m.PLUGIN_DESCRIPTION, help=m.PLUGIN_HELP)
        )
    args = parser.parse_args(["config", "get", '-k', "mac"])
    if not vars(args):
        parser.print_usage()
    else:
        args.func(args, _CONTEXT)


if __name__ == "__main__":
    main()
