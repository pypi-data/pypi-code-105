from setuptools import setup

setup(
    name='sapipy',
    version='0.1.1',    
    description='A Python interface for the Solar Analytics API',
    long_description='A Python interface for the Solar Analytics API',
    url='https://github.com/aws404/sapipy',
    author='aws404',
    author_email='aws40404@gmail.com',
    license='GNU GPLv3',
    packages=['sapipy'],
    install_requires=['requests']
)