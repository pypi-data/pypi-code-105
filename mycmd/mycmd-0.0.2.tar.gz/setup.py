from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()


with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='mycmd',
    version='0.0.2',
    author='Andrija Vojnovic',
    author_email='andrija.vojnovic@cyberlab.rs',
    url='https://github.com/cyberlabrs/my-commands-cli',
    description='CLI for My Command Service.',
    long_description=readme,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mycmd = command_service.main:main'
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    keywords='cyberlab my command  python package ',
    install_requires=requirements,
    zip_safe=False
)