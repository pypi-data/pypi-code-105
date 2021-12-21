VERSION = {
    'major': 0,
    'minor': 0,
    'micro': 2}


def get_version_string():
    version = '{major}.{minor}.{micro}'.format(**VERSION)
    return version


__version__ = get_version_string()
