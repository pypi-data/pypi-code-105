from setuptools import setup, find_packages
long_description= '''Python module for interpolation and approximation'''
requirements=["fraction","numpy","matplotlib","scipy","numexpr","mpmath"]
setup(name='interpop',
      version='1.8',
      url='https://github.com/danial29rus/interpop',
      license='MIT',
      author='danial29rus',
      author_email='shpeka4kaps4@mail.ru',
      install_requires=requirements,
      zip_safe=False)