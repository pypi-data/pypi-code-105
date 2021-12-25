from setuptools import setup, find_packages
long_description= '''Python module for solve intepolation and approximation'''
requirements=["fraction","numpy","matplotlib","scipy","numexpr","mpmath","pylab"]
setup(name='intepop',
      version='1.0',
      url="https://github.com/danial29rus/interpop",
      license='MIT',
      author='danial29rus',
      author_email='shpeka4kaps4@mail.ru',
      install_requires=requirements,
      zip_safe=False)