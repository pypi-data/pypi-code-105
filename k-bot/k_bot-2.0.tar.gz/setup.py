from setuptools import setup, find_packages


setup(name             = 'k_bot',
    version          = '2.0',
    description      = '한국 디스코드봇 리스트 api를 더욱 쉽게! | Korean Discord bot list api easier!',
    long_description = open('README.md').read(),
    author           = '5-23',
    author_email     = 'yhanbyeol6@gmail.com',
    url              = 'https://github.com/5-23/k_bot/tree/main',
    download_url     = 'https://github.com/5-23/k_bot/tree/main',
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