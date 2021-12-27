from setuptools import setup

setup(
    name='packageLab2Sets',
    version='0.1',
    description='Conflict package for Lab2',
    url='',
    install_requires=['pandas<1.0'], # требуем версию < 1.0 для конфликта
    packages=['packageLab2'],
)
