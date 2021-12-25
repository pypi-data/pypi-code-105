from setuptools import setup, find_packages
long_description= '''Python module for solve ODE'''
requirements=["fraction","numpy","matplotlib","scipy"]
setup(name='oderk',
      version='1.2',
      url='https://github.com/danial29rus/oderk',
      license='MIT',
      author='danial29rus',
      author_email='shpeka4kaps4@mail.ru',
      install_requires=requirements,
      zip_safe=False)