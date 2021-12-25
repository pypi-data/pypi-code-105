from setuptools import setup, find_packages


setup(
    name='regression-transform-helpers',
    version='0.0.1',
    license='MIT',
    author="Nick Yazdani",
    author_email='nnyazdani92@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Nick-Yazdani/regression-transform-helpers',
    keywords='regression transformers helpers',
    install_requires=[
          'scikit-learn',
          'joblib',
          'numpy'
      ],

)