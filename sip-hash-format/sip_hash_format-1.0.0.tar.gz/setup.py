from distutils.core import setup
from setuptools import find_packages


with open("README.rst", "r") as f:
  long_description = f.read()


setup(name='sip_hash_format',
      version='1.0.0',
      description='encoding for xuhui_sip',
      long_description=long_description,
      author='wen2zhou',
      author_email='fearless82@163.com',
      url='https://pypi.org/',
      install_requires=[],
      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Topic :: Software Development :: Libraries'
      ],
    )
