from setuptools import setup, find_packages

setup(name='nummethvera', 
      version='0.1.5', 
      url='https://github.com/dthseemsbttr/numericmethodsdths', 
      license='MIT', 
      author='Vera Korotkova',
      author_email='verakorotkova10@mail.ru', 
      description='Numeric methods library',
      packages=['nummethvera'],
      long_description=open('README.md').read(),
      setup_requires=['sympy>=1.6.2', 'mpmath>=1.1.0', 'scipy>=1.5.2',
                      'numpy>=1.19.2,<1.21', 'matplotlib>=3.5.0',
                      'PyWavelets>=1.1.1', 'numba>=0.51.2',
                      'networkx>=2.5'],
      zip_safe=False)