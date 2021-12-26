from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='less-learn-mpi',
      version='0.1.2',
      description='Learning with Subset Stacking - MPI',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/sibirbil/LESS-MPI',
      maintainer='Kaya Gokalp',
      maintainer_email='kayagokalp@sabanciuniv.edu',
      license='MIT',
      packages=['lessmpi'],
      zip_safe=False,
      python_requires='>=3.6',
      install_requires=[
        'mpi4py>=3.0.0',
        'scikit-learn>=1.0.1',
        'numpy>=1.21.4'
      ])
