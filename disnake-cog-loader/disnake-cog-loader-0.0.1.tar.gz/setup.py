import pathlib
from setuptools import setup

ROOT = pathlib.Path(__file__).parent

with open(ROOT / 'README.md', 'r', encoding='utf-8') as f:
    README = f.read()

setup(
    name='disnake-cog-loader',
    author='Myxi',
    url='https://github.com/m-y-x-i/disnake-cog-loader',
    version='0.0.1',
    packages=['disnake.ext.loader'],
    description='An extension module for disnake to load cogs without needing the setup function.',
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=['disnake'],
    python_requires='>=3.8.0'
)