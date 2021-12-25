import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'strings-utils',
    version = '0.0.2',
    author = 'Andrea Princic',
    author_email = 'princic.1837592@studenti.uniroma1.it',
    description = 'Utilities for multi-language projects',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/Princic-1837592/strings-utils',
    packages = setuptools.find_packages(),
    python_requires = '>=3.6',
)
