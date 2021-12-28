from distutils.core import setup
from setuptools import find_packages

with open("README.txt", "r") as f:
  long_description = f.read()

setup(name='shopex_matrix_tools',  # 包名
      version='1.4.0',  # 版本号
      description='shopex_matrix_tools',
      long_description=long_description,
      author='xuhongtao',
      author_email='18921846960@163.com',
      url='https://git.ishopex.cn/matrix-container/matrix_tools.git',
      install_requires=['pika==1.1.0', 'pymongo==3.4.0'],
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
          'Topic :: Software Development :: Libraries'
      ],
      )