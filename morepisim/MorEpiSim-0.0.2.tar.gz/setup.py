
from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='MorEpiSim',
  version='0.0.2',
  description='a Reinforcement Learning based Epidemic control simulation environment',
  long_description=open('README.rst').read(),
  url='',  
  author='M.A.CHADI',
  author_email='m.aminechadi@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='RL_based_Epidemic_control', 
  packages=["MorEpiSim"],
  include_package_data=True,
  #packages= find_packages(),
  install_requires=['numpy', 'matplotlib', 'networkx', 'gym']
                      # and openCV, imageIO : for play_and_save_video()
)
