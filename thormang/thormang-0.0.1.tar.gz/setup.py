import setuptools
from pathlib import Path

setuptools.setup(
    name='thormang',
    version='0.0.1',
    description="A OpenAI Gym Env for thormang",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="thormang*"),
    install_requires=['gym']  # And any other dependencies thormang needs
)