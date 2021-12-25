from setuptools import setup, find_packages

def readme() -> str:
    with open(r'README.md') as f:
        README = f.read()
    return README

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Science/Research',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='linearregressor',
    version='0.0.1',
    description='Module of numerical statistic prediction using linear regression by determinant matrix method with intercept, slope, correlation coefficient, and determination coefficient calculations',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/zaafirrahman/linearregressor',
    author='Zaafirrahman',
    author_email='zaafir123rahman@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['linear regression', 'machine learning', 'prediction'],
    packages=find_packages(),
    install_requires=['']
)