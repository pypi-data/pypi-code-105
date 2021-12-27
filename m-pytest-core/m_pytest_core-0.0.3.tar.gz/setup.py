from setuptools import setup

setup(
    name='m_pytest_core',
    version='0.0.3',
    packages=['m_pytest_core', 'm_pytest_core.core', 'm_pytest_core.core.db', 'm_pytest_core.core.utils',
              'm_pytest_core.files'],
    url='https://github.com/AlekseiMiasnikov/pytest_core',
    license='Free',
    author='myasnikov_am',
    author_email='lexalightning@gmail.com',
    description='The framework core from pytest.'
)
