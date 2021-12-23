from setuptools import setup


with open("README.md", "r") as long_descr:
    long_description = long_descr.read()

setup(
    name = 'Peji',
    version = '1.0.2',
    author = 'ge',
    description = 'Static site generator.',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://peji.gch.icu/',
    classifiers = [
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.6',
    py_modules = ['peji'],
    install_requires = [
        'click',
        'markdown',
        'Jinja2',
        'Pygments',
        'PyYAML'
    ],
    entry_points = {
        'console_scripts': [
            'peji = peji:cli'
        ]
    }
)
