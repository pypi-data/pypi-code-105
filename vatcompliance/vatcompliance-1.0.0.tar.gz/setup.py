from setuptools import setup

setup(
    name='vatcompliance',
    version='1.0.0',
    packages=['vatcompliance'],
    url='https://vatcompliance.co/',
    license='MIT License',
    author='vatcompliance',
    author_email='info@vatcompliance.co',
    description='Vatcompliance API client for Python',
    install_requires=[
        'requests >= 2.13.0',
    ],
)
