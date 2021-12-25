from setuptools import setup, find_packages
long_description= '''Python module for solve matrix by gauss and Jacoby'''
requirements=["fraction","numpy","matplotlib","scipy","numexpr","mpmath"]
setup(name='odeshp',
      version='1.6',
      url='https://github.com/danial29rus/odeshp',
      license='MIT',
      author='danial29rus',
      author_email='shpeka4kaps4@mail.ru',
      install_requires=requirements,
      zip_safe=False)