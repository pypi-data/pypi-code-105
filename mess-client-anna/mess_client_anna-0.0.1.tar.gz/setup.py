from setuptools import setup, find_packages

setup(name="mess_client_anna",
      version="0.0.1",
      description="mess_client_anna",
      author="Anna M.",
      author_email="an.malch@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )