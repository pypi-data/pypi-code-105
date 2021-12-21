from distutils.core import setup
import re
from os.path import dirname, join


def get_version(version_file):
    pattern = r"^__version__ = ['\"]([^'\"]*)['\"]"
    match = re.search(pattern, open(version_file, "rt").read(), re.MULTILINE)
    if match:
        return match.group(1)

    raise RuntimeError("Unable to find version string in %s." % (version_file,))


def read_file(filename):
    with open(join(dirname(__file__), filename)) as f:
        return f.read()


setup(
    name='guesstidate',
    version=get_version("guesstidate/__init__.py"),
    packages=['guesstidate'],
    url='https://github.com/Fraunhofer-FIT-DSAI-PM/guesstidate',
    license='Apache 2.0',
    author='Fraunhofer FIT',
    author_email='sebastiaan.van.zelst@fit.fraunhofer.de, alessandro.berti@fit.fraunhofer.de',
    description="Infers date format from examples"
)
