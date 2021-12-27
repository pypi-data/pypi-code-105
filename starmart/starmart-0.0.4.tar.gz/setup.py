from distutils.core import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='starmart',
    packages=['starmart'],
    version='0.0.4',
    license='apache-2.0',
    description='Starmart deployment tool',
    author='Tomas Piaggio',
    author_email='tomaspiaggio@starmart.io',
    url='https://starmart.io',
    keywords=['AI', 'Machine Learning', 'Deep Learning', 'Serverless'],
    install_requires=[
        'GitPython==3.1.24',
        'flask==2.0.2',
        'waitress==2.0.0',
        'python-dotenv==0.19.2',
        'halo==0.0.31',
        'cryptography==36.0.1'
    ],
    scripts=['bin/starmart'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
