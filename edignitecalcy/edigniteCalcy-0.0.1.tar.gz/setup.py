from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='edigniteCalcy',
    version='0.0.1',
    description='A good python library by Prince Verma for an Edignite Ngo to perform math operation like Additon, Subtraction and Multiplication or  Divison etc.',
    long_description=open('README.txt').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='',
    author='Prince Verma',
    author_email='princevermasrcc@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='calculator, edigniteNgo, princeverma, calcy',
    packages=find_packages(),
    install_requires=['']
)
