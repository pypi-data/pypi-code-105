from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='django_pmedien_export',
    version='0.21',
    packages=find_packages(exclude=['tests*']),
    py_modules=['django_pmedien_export'],
    license='MIT',
    description='General export for a complete model with languages',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['django >= 1.11'],
    url='http://www.pmedien.com',
    author='pmedien GmbH',
    author_email='nomail@pmedien.com',
    python_requires=">=2.7",
)