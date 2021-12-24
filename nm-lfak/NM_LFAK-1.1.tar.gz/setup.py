from setuptools import setup, find_packages

requirements = ['numpy>=1.19.2']
setup(name='NM_LFAK',
      version='1.1',
      description='Numerical methods',
      packages=find_packages(),
      author_email='vovalagutov1111@yandex.ru',
      install_requieres = requirements,
      zip_safe=False,
      )