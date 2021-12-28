from setuptools import (
    find_packages,
    setup
)

INSTALL_REQUIRES = (
    'pandas'
)

setup(
    name='road_collisions_base',
    version='0.0.1',
    python_requires='>=3.6',
    description='Road collision base',
    author='Robert Lucey',
    url='https://github.com/RobertLucey/road-collisions-base',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': [
            'load_road_collisions = road_collisions_base.bin.load:main'
        ]
    }
)
