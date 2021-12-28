import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pygpsparser',
    version='0.0.5',
    author='Kun-Neng Hung',
    author_email='kunneng.hung@gmail.com',
    description='GPS Sentence Parser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Kun-Neng/py-gps-parser',
    packages=setuptools.find_packages(),
    install_requires=[
        'pytz',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6'
)
