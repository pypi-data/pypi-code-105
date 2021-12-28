from setuptools import setup, find_packages

setup(
    name="polska",
    version="1.1",
    description="Пакет для перевода выражения в обратную польскую запись",
    author="Demekhina Arina",
    author_email="ademkhina@list.ru",
    packages=find_packages(),
    install_requires=['pytest==6.2.5'],
    include_package_data=True)
