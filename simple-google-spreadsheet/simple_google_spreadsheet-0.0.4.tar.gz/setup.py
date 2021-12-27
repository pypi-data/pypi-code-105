import setuptools

_name = 'simple_google_spreadsheet'
_desc = 'A module class to simplify the integration of your data with a sheet in Google SpreadSheet'
_url = 'https://github.com/mbiemann/simple-google-spreadsheet'
_reqs = [
    'google-api-python-client',
    'google-auth-httplib2',
    'google-auth-oauthlib',
]

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()
long_description = str(long_description) + '\n___\n' + 'Check on GitHub: ' + '\n' + _url

setuptools.setup(
    name=_name,
    version='0.0.4',
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