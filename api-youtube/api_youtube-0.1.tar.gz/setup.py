from setuptools import setup, find_packages


setup(name             = 'api_youtube',
    version          = '0.1',
    description      = '유튜브 api를 더욱 쉽게! | youtube api easier!',
    long_description = open('README.md').read(),
    author           = '5-23',
    author_email     = 'yhanbyeol6@gmail.com',
    url              = 'https://github.com/5-23/api_youtube',
    download_url     = 'https://github.com/5-23/api_youtube',
    install_requires = ['requests'],
    packages         = find_packages(exclude = ['docs', 'example']),
    keywords         = ['bot', 'study', 'api'],
    python_requires  = '>=3',
    zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)