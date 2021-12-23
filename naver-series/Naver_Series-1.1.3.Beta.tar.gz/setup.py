from setuptools import setup, find_packages

setup(
    name='Naver_Series',
    version='1.1.3 Beta',
    description='Naver Series module',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    author='EGGnmad',
    author_email='viewnono1219@gmail.com',
    url='https://github.com/EGGnmad/NaverSeries',

    packages=find_packages(),
    keywords=['Naver', 'Naver Series', 'Book'],

    install_requires=['requests==2.26.0', 'beautifulsoup4==4.10.0']
)