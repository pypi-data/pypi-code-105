# -*- coding: utf-8 -*-

from codecs import open
from setuptools import setup
import re

with open('osmapipy2/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

try:
    import pypandoc
    from unidecode import unidecode
    description = open('README.md', encoding='utf-8').read()
    description = unidecode(description)
    description = pypandoc.convert(description, 'rst', format='md')
except (IOError, OSError, ImportError):
    description = 'Python wrapper for the OSM API'

setup(
    name='osmapi-py2',
    packages=['osmapipy2'],
    version=version,
    install_requires=['requests'],
    description='Python 2 wrapper for the OSM API',
    long_description=description,
    long_description_content_type='text/x-rst',
    maintainer='Fisher Tsai',
    maintainer_email='fishy0903@gmail.com',
    url='https://github.com/fishertsai/osmapi-py2',
    keywords=['openstreetmap', 'osm', 'api'],
    license='GPLv3',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
