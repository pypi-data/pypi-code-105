from setuptools import setup, find_packages

setup(
    name='Naver_Series',
    version='1.1.0 Beta',
    description='Naver Series module',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    author='EGGnmad',
    author_email='viewnono1219@gmail.com',
    url='https://github.com/EGGnmad/NaverSeries',

    packages=find_packages(),
    keywords=['Naver', 'Naver Series', 'Book'],

    requires=['requests', 'beautifulsoup4']
)