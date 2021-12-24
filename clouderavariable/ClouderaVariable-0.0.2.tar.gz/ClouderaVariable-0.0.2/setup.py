from setuptools import setup, find_packages
setup(name='ClouderaVariable',
      version='0.0.2',
      description='Configuration path information of Cloudera related components',
      author='zhuhs',
      author_email='zhuhs087@163.com',
      requires= ['numpy'],
      packages=find_packages(),
      license="apache 3.0"
      )