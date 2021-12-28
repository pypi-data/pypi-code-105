from setuptools import setup, find_packages

setup(
    name='django_pmedien_defaults',
    version='0.10',
    packages=find_packages(exclude=['tests*']),
    py_modules=['django_pmedien_defaults'],
    license='MIT',
    description='Skip list view to make a simple confguration entry in a table',
    long_description='Skip list view to make a simple confguration entry in a table',
    install_requires=['django >= 1.11'],
    url='http://www.pmedien.com',
    author='pmedien GmbH',
    author_email='nomail@pmedien.com',
    python_requires=">=2.7",
)