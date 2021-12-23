"""setup file for places geocoding package"""
from setuptools import setup, find_packages
import setuptools
from pathlib import Path
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy as np
import numpy
import importlib.machinery
this_directory = Path(__file__).parent

VERSION = '0.4.2'
DESCRIPTION = 'Package for Places Geocoding API service'

extensions = [
    Extension('address_packet', ["address_packets.pyx"], include_dirs=[numpy.get_include()]),
    Extension('certainty_search', ["certainty_searchs.pyx"], include_dirs=[numpy.get_include()]),
    Extension('check_address_length', ['check_address_lengths.pyx'], include_dirs=[numpy.get_include()]),
    Extension('check_dups', ['check_dupss.pyx'], include_dirs=[numpy.get_include()]),
    Extension('check_lat_long_length', ['check_lat_long_lengths.pyx'], include_dirs=[numpy.get_include()]),
    Extension('coordinate_conv_package', ['coordinate_conv_packages.pyx'], include_dirs=[numpy.get_include()]),
    Extension('create_convex_array', ['create_convex_arrays.pyx'], include_dirs=[numpy.get_include()]),
    Extension('create_convex_elastic', ['create_convex_elastics.pyx'], include_dirs=[numpy.get_include()]),
    Extension('executor_unpack', ['executor_unpacks.pyx'], include_dirs=[numpy.get_include()]),
    Extension('null_parameters', ['null_parameterss.pyx'], include_dirs=[numpy.get_include()]),
    Extension('radius_arr', ['radius_arrs.pyx'], include_dirs=[numpy.get_include()]),
    Extension('reverse_spreadsheet', ['reverse_spreadsheets.pyx'], include_dirs=[numpy.get_include()]),
    Extension('spreadsheet_c', ['spreadsheet_cs.pyx'], include_dirs=[numpy.get_include()]),
    Extension('TFIDF_max', ['TFIDF_maxs.pyx'], include_dirs=[numpy.get_include()]),
    Extension('TFIDF_max_elastic', ['TFIDF_max_elastics.pyx'], include_dirs=[numpy.get_include()]),
    Extension('TFIDF_upgraded', ['TFIDF_upgradeds.pyx'], include_dirs=[numpy.get_include()]),
    Extension('zip_coordinate', ['zip_coordinates.pyx'], include_dirs=[numpy.get_include()]),
    Extension('zip_coordinates_elastic', ['zip_coordinates_elastics.pyx'], include_dirs=[numpy.get_include()])
]

# Setting up
setup(
    name="places_geocode",
    version=VERSION,
    author="Martin Mashalov",
    author_email="hello@places.place",
    description=DESCRIPTION,
    long_description=open('/Users/martinmashalov/Documents/places_geocoding_package/README.md').read(),
    long_description_content_type="text/markdown",
    packages=['places_geocode', 'places_geocode/app', 'places_geocode/Logs', 'places_geocode/app/models', 'places_geocode/app/CythonOperations', 'places_geocode/app/dprk_copy'],
    license="MIT",
    ext_modules=cythonize(extensions, build_dir="places_geocode/app/CythonOperations"),
    #include_dirs=np.get_include(),
    url="https://medium.com/p/10cc24c34505/edit",
    install_requires=['pymongo', 'numpy', 'pandas', 'sklearn', 'dependency_injector', 'pydantic', 'fastapi', 'cython',
                      'state_machine', 'elasticsearch', 'usaddress', 'nltk'],
    keywords=['python',
              'geocoding',
              'forward geocoding',
              'reverse geocoding',
              'radius loading',
              'loading radius',
              'autocomplete',
              'places of interest',
              'POI'
              ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: Free for non-commercial use",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)