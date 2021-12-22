from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Sajal-Image-Processing',
  version='0.0.1',
  description='A very basic Image Processing',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Sajal Garg',
  author_email='sajalgarg17.sg@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='imageprocessing', 
  packages=find_packages(),
  install_requires=['opencv-python'] 
)