from setuptools import setup, find_packages
import codecs
import os

current_path = os.getcwd()


def full_path(path):
    return os.path.join(current_path, path)


VERSION = '1.0.2'
DESCRIPTION = 'A Python package for the creation of a CPM project.'

# setting up the project
setup(
    name="cpp-projects-manager-cli",
    version=VERSION,
    author="Aashish Panchal",
    author_email="aipanchal51@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=codecs.open(os.path.join(
        os.path.dirname(__file__), 'README.md'), 'r', 'utf-8').read(),
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["cpmIcon.txt", ".gitignore", "LICENSE", "README.md", full_path("cpm/conf/app_template/include/app_name.hpp-tpl"), full_path("cpm/conf/app_template/source/app_name.cpp-tpl"), full_path("cpm/conf/app_template/app_name.cpp-tpl"), full_path("cpm/conf/project_template/entry_point.cpp-tpl")],
    },
    install_requires=[],
    keywords=["cpm", "c++ with python"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
