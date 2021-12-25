__version__ = '0.21'


def version_hook(config):
    config['metadata']['version'] = __version__
