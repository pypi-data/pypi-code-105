from setuptools import setup

setup(
    name='dickey_fuller_test',
    version='0.2.0',
    description='Module for Lab2, DA',
    url='https://twitter.com/vsklamm',
    author='Sergey Vasilchenko',
    author_email='klammvs@google.com',
    packages=['dickey_fuller_test'],
    install_requires=[
        'numpy>=1.19',
        'matplotlib>=3.4',
        'statsmodels>=0.13'
    ],
    setup_requires=[
        'numpy>=1.19',
        'matplotlib>=3.4',
        'statsmodels>=0.13'
    ],
)
