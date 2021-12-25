"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

license = (here / 'LICENSE.txt').read_text(encoding='utf-8')

setup(
    name='hogpylib',
    version='1.0.0',
    description='Histogram of Gradients in Python from scratch',
    url='https://github.com/shubhamwagh/HOG_python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=license,
    platforms=['Ubuntu 20.04', 'Windows'],
    author='Shubham Wagh',
    author_email='shubhamwagh48@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10",
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='PyHOG, setuptools, development',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=['scikit-image'],
    data_files=[('data', ['data/car.jpg', 'data/people.jpg']), ('examples', ['examples/Hog_car.png', 'examples/HOG_people.png', 'examples/HOG_implementation.png'])],
    entry_points={
        'console_scripts': [
            'hogpylib=hogpylib.__main__:main',
        ],
    },
)
