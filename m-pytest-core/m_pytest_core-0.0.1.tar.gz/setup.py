from setuptools import setup

setup(
    name='m_pytest_core',
    version='0.0.1',
    description='The framework core from pytest.',
    install_requires=['allure-pytest', 'allure-python-commons', 'testrail-api', 'SQLAlchemy'],
    packages=['m_pytest_core'],
    url='https://github.com/AlekseiMiasnikov/pytest_core.git',
)
