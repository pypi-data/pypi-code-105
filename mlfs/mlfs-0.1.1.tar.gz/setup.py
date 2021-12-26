from setuptools import setup

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='mlfs',
    version='0.1.1',    
    description='A package for maximum likelihood density fitting and simulation.',
    url='https://github.com/romanov360/mlfs',
    author='Tristan Romanov',
    author_email='romanov360@gmail.com',
    license='BSD 2-clause',
    packages=['mlfs'],
    install_requires=[],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: OS Independent',        
        'Programming Language :: Python',
    ],
)