import setuptools

_name = 'simple_toolbelt'
_desc = 'A growing collection of simple utilities functions for Python'
_url = 'https://github.com/mbiemann/python-simple-toolbelt'
_reqs = []

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()
long_description = str(long_description) + '\n___\n' + 'Check on GitHub: ' + '\n' + _url

setuptools.setup(
    name=_name,
    version='0.0.2',
    author='Marcell Biemann',
    author_email='mbiemann@gmail.com',
    description=_desc,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=_url,
    project_urls={
        'Bug Tracker': _url + '/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=[_name],
    python_requires='>=3.6',
    install_requires=_reqs
)