# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(name="autoxtest",
        version="0.1.0",
        description="automl for competition",
        author="caihengxing",
        author_email="caihengxing@4paradigm.com",
        url='https://github.com/4paradigm/autox',
        install_requires=[
            # 'lightgbm',
            # 'xgboost',
            # 'pytorch-tabnet',
            # 'torch',
            'numpy',
            'pandas',
            # 'sklearn',
            'tqdm',
            # 'optuna',
            # 'img2vec_pytorch'
        ],
        python_requires='>=3.6',
        # packages=[],
        packages=find_packages(exclude=['data','run.py']),
        #ext_modules=cythonize("cli_examples/primes.pyx"), #Cython extension demo
        #package_data={"cli_examples": ["prmies.pyx"]}, #force sdist to keep the .pyx files
        include_package_data=True,
        zip_safe=False # not install as zip file
        )
