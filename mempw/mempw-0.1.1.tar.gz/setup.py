# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='mempw',
      version='0.1.1',
      description='Python-based memorable password generator',
      long_description=('Generates pronouncable passwords '
                        'based on system wordlists'),
      author='Mark Thurston',
      author_email='mark@mdvthu.com',
      url='https://github.com/mdvthu/mempw',
      license='Apache License Version 2.0',
      packages=['mempw'],
      scripts=['scripts/mempw'])
