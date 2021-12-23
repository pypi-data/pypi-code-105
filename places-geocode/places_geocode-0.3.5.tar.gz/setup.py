"""setup file for places geocoding package"""
from setuptools import setup, find_packages
import setuptools
from pathlib import Path
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy as np
import importlib.machinery
this_directory = Path(__file__).parent

VERSION = '0.3.5'
DESCRIPTION = 'Package for Places Geocoding API service'

extensions = [
    Extension('address_packet', ["address_packet.pyx", 'places_geocode/app/CythonOperations/address_packet.c']),
    Extension('certainty_search', ["certainty_search.pyx", 'places_geocode/app/CythonOperations/certainty_search.c']),
    Extension('check_address_length', ['check_address_length.pyx', 'places_geocode/app/CythonOperations/check_address_length.c']),
    Extension('check_dups', ['check_dups.pyx', 'places_geocode/app/CythonOperations/check_dups.c']),
    Extension('check_lat_long_length', ['check_lat_long_length.pyx', 'places_geocode/app/CythonOperations/check_lat_long_length.c']),
    Extension('coordinate_conv_package', ['coordinate_conv_package.pyx', 'places_geocode/app/CythonOperations/coordinate_conv_package.c']),
    Extension('create_convex_array', ['create_convex_array.pyx', 'places_geocode/app/CythonOperations/create_convex_array.c']),
    Extension('create_convex_elastic', ['create_convex_elastic.pyx', 'places_geocode/app/CythonOperations/create_convex_elastic.c']),
    Extension('executor_unpack', ['executor_unpack.pyx', 'places_geocode/app/CythonOperations/executor_unpack.c']),
    Extension('null_parameters', ['null_parameters.pyx', 'places_geocode/app/CythonOperations/null_parameters.c']),
    Extension('radius_arr', ['radius_arr.pyx', 'places_geocode/app/CythonOperations/radius_arr.c']),
    Extension('reverse_spreadsheet', ['reverse_spreadsheet.pyx', 'places_geocode/app/CythonOperations/reverse_spreadsheet.c']),
    Extension('spreadsheet_c', ['spreadsheet_c.pyx', 'places_geocode/app/CythonOperations/spreadsheet_c.c']),
    Extension('TFIDF_max', ['TFIDF_max.pyx', 'places_geocode/app/CythonOperations/TFIDF_max.c']),
    Extension('TFIDF_max_elastic', ['TFIDF_max_elastic.pyx', 'places_geocode/app/CythonOperations/TFIDF_max_elastic.c']),
    Extension('TFIDF_upgraded', ['TFIDF_upgraded.pyx', 'places_geocode/app/CythonOperations/TFIDF_upgraded.c']),
    Extension('zip_coordinate', ['zip_coordinate.pyx', 'places_geocode/app/CythonOperations/zip_coordinate.c']),
    Extension('zip_coordinates_elastic', ['zip_coordinates_elastic.pyx', 'places_geocode/app/CythonOperations/zip_coordinates_elastic.c'])
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
    packages=['places_geocode', 'places_geocode/app', 'places_geocode/Logs', 'places_geocode/app/models', 'places_geocode/app/CythonOperations', 'places_geocode/app/dprk_copy', 'places_geocode/app/CythonOperations/places_geocode/app/dprk_copy'],
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