from setuptools import setup, find_packages

long_description= """Зачёт"""

setup(name='Chislov',
      version='0.1',
      url='https://github.com/NooODZy/Chislov',
      license='MIT',
      packages=find_packages(),
      author='Fedor987',
      author_email='antonvalentini40@gmail.com',
      install_requires = ['numpy','skipy','sympy','webbrowser', 'copy' 'fractions'],
      zip_safe=False)