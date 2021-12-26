from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

VERSION = "1.0"
README_PATH = "./README.md"

# test_requirements = ["behave", "behave-classy", "pytest"]

long_description = ""
with open(README_PATH, "r", encoding="utf-8") as file:
    long_description = file.read()


setup(
    name="AloggerPy",
    version=VERSION,
    license="Apache Software License 2.0",
    description="Python colored logger module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ahmet KÖKEN",
    author_email="ahmetkkn07@gmail.com",
    url="https://github.com/ahmetkkn07/Alogger",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Utilities",
    ],
    project_urls={
        "Changelog": "https://github.com/ahmetkkn07/Alogger",
        "Issue Tracker": "https://github.com/ahmetkkn07/Alogger/issues",
    },
    keywords=[],
    # python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    # install_requires=["requests"],  # Bağlı olduğu paketler, örn: requests
    extras_require={
        # eg:
        #   "rst": ["docutils>=0.11"],
        #   ":python_version=="2.6"": ["argparse"],
    },
    # setup_requires=[
    #     "pytest-runner",
    # ],
    entry_points={
        # Komut isteminden çalıştırma
        # örndeğin: ypackage
        # Kullanım: "ypacakge = ypackage.ypackage:main
        "console_scripts": [
            "ygitbookintegration = ypackage.cli.integrate_into_gitbook:main",
            "ygoogledrive = ypackage.cli.gdrive:main",
            "ygooglesearch = ypackage.cli.gsearch:main",
            "yfilerenamer = ypackage.cli.file_renamer:main",
            "ythemecreator = ypackage.cli.theme_creator:main"
        ]
    },
    # tests_require=test_requirements,
)
