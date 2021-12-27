from setuptools import setup, find_packages 

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: MacOS :: MacOS X',
    'License :: OSI Approved :: MIT License',
    "Programming Language :: Python :: 3",
]

setup(
    name='endist',
    version='0.0.3',
    description='A Python library for the distribution system operations',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',
    url='',
    author='Blaž Dobravec',
    email='blaz@dobravec.si',
    license='MIT',
    classifiers=classifiers,
    packages=find_packages(),
    install_requires=[''],
    python_requires='>=3.6',
)