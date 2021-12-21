from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='StoaCalculator',
    version='0.1.3',
    description='Stoa Calculator is a powerful calculator that have everything you need to do any kind of calculations!',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    url='https://jorgeeldis.me',
    author='Jorge Eldis Gonzalez',
    author_email='jorgeeldisg30@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='calculator',
    packages=find_packages(),
    install_requires=['']
)
