#! /usr/bin/env python
import glob
from setuptools import setup, Extension

setup(
    name="DAWG-Patched",
    version="0.9.1",
    description="Fast and memory efficient DAWG (DAFSA) for Python",
    long_description=open('README.rst').read() + '\n\n' + open('CHANGES.rst').read(),
    author='Taketomo Isazawa',
    author_email='taketomo.isazawa@gmail.com',
    url='https://github.com/ti250/DAWG-patched',

    ext_modules=[
        Extension(
            "dawg",
            sources=glob.glob('src/*.cpp') + glob.glob('lib/b64/*.c'),
            include_dirs=['lib'],
            language="c++",
        )
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Cython',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
    ],
)
