#!/usr/bin/env python

from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(name='magicpy',
      version='0.1.1',
      description='Toolbox to control MagVenture TMS stimulators',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Ole Numssen',
      author_email='numssen@posteo.de',
      project_urls={'Home': 'https://gitlab.gwdg.de/tms-localization/utils/magicpy',
                    'Docs': 'https://magicpy.readthedocs.io/',
                    'Twitter': 'https://twitter.com/num_ole',
                    'Download': 'https://pypi.org/project/numpy/'},
      packages=['magicpy'],
      install_requires=['pyserial>=3.5', 'numpy>=1.20.0'],
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Science/Research',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Software Development :: Build Tools',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9', ]
      )
