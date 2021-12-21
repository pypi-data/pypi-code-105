#!/usr/bin/env python

from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(name='magicpy',
      version='0.0.1',
      description='Toolbox to control MagVenture TMS stimulators',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Ole Numssen',
      author_email='numssen@posteo.de',
      url='https://gitlab.gwdg.de/tms-localization/utils/magicpy',
      packages=['magicpy'],
      install_requires=['pyserial>=3.5', 'numpy>=1.20.0']
      )
