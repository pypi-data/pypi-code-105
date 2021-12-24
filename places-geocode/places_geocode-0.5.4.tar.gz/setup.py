"""setup file for places geocoding package"""
from setuptools import setup, find_packages
import setuptools
from pathlib import Path
from distutils.core import setup
from distutils.extension import Extension
try:
    from Cython.Build import cythonize
except ModuleNotFoundError:
    raise Exception("install 'cython' before installing places-geocode")
import numpy as np
try:
    import numpy
except ModuleNotFoundError:
    raise Exception("install 'numpy' before installing places-geocode")
import importlib.machinery

this_directory = Path(__file__).parent

VERSION = '0.5.4'
DESCRIPTION = 'Package for Places Geocoding API service'

extensions = [
    Extension(name='address_packet', sources=["address_packets.pyx"], library_dirs=["./places_geocode/app/CythonOperations"],
            include_dirs=["./places_geocode/app/CythonOperations"], runtime_library_dirs=["./places_geocode/app/CythonOperations"]),
    Extension('certainty_search', ["certainty_searchs.pyx"], library_dirs=["."],
            include_dirs=["."], runtime_library_dirs=["."]),
    Extension('check_address_length', ['check_address_lengths.pyx'], library_dirs=["."],
            include_dirs=["."], runtime_library_dirs=["."]),
    Extension('check_dups', ['check_dupss.pyx'], library_dirs=["."],
            include_dirs=["."], runtime_library_dirs=["."]),
    Extension('check_lat_long_length', ['check_lat_long_lengths.pyx'], library_dirs=["."],
            include_dirs=["."], runtime_library_dirs=["."]),
    Extension('coordinate_conv_package', ['coordinate_conv_packages.pyx'], library_dirs=["."],
            include_dirs=["."], runtime_library_dirs=["."]),
    Extension('create_convex_array', ['create_convex_arrays.pyx'], library_dirs=["."],
            include_dirs=["."], runtime_library_dirs=["."]),
    Extension('create_convex_elastic', ['create_convex_elastics.pyx'], library_dirs=["."],
            include_dirs=["."], runtime_library_dirs=["."]),
    Extension('executor_unpack', ['executor_unpacks.pyx'], library_dirs=["."],
            include_dirs=["."], runtime_library_dirs=["."]),
    Extension('null_parameters', ['null_parameterss.pyx'], library_dirs=["."],
            include_dirs=["."], runtime_library_dirs=["."]),
    Extension('radius_arr', ['radius_arrs.pyx'], library_dirs=["."],
            include_dirs=["."], runtime_library_dirs=["."]),
    Extension('reverse_spreadsheet', ['reverse_spreadsheets.pyx'], library_dirs=["."],
            include_dirs=["."], runtime_library_dirs=["."]),
    Extension('spreadsheet_c', ['spreadsheet_cs.pyx'], library_dirs=["."],
            include_dirs=["."], runtime_library_dirs=["."]),
    Extension('TFIDF_max', ['TFIDF_maxs.pyx'], library_dirs=["."],
            include_dirs=["."], runtime_library_dirs=["."]),
    Extension('TFIDF_max_elastic', ['TFIDF_max_elastics.pyx'], library_dirs=["."],
            include_dirs=["."], runtime_library_dirs=["."]),
    Extension('TFIDF_upgraded', ['TFIDF_upgradeds.pyx'], library_dirs=["."],
            include_dirs=["."], runtime_library_dirs=["."]),
    Extension('zip_coordinate', ['zip_coordinates.pyx'], library_dirs=["."],
            include_dirs=["."], runtime_library_dirs=["."]),
    Extension('zip_coordinates_elastic', ['zip_coordinates_elastics.pyx'], library_dirs=["."],
            include_dirs=["."], runtime_library_dirs=["."])
]

# Setting up
setup(
    name="places_geocode",
    version=VERSION,
    author="Martin Mashalov",
    author_email="hello@places.place",
    description=DESCRIPTION,
    long_description=open('README.md').read(),
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