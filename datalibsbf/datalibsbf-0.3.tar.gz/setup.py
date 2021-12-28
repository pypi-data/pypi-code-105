from setuptools import setup, find_packages
 
setup(name='datalibsbf',
      version='0.3',
      url='https://github.com/grupo-sbf/data-libs',
      author='Matheus Beltrão',
      author_email='matheus.beltrao@gruposbf.com.br',
      description='Lib de disponibilizacao de funcoes genericas criadas dentro do time de dados',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False)