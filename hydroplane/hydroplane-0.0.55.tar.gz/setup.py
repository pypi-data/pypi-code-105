import pathlib
from setuptools import setup, find_packages

# # The directory containing this file
# HERE = pathlib.Path(__file__).parent

# # The text of the README file
# README = (HERE / "README.md").read_text()

setup(
   name='hydroplane',
   version='0.0.55',
   author='Ryan Moos',
   author_email='ryan@moos.engineering',
   packages=find_packages(),
   scripts=['bin/hydro'],
   url='http://pypi.python.org/pypi/hydroplane/',
   license='LICENSE',
   description='A Data Exploration Custom Dashboarding Framework',
   long_description=open('README.md').read(),
   long_description_content_type='text/markdown',
   include_package_data=True,
   install_requires=[
       "dash", 
       "pandas",
       "numpy",
       "cython",
       "pydruid",
       "requests",
       "psycopg2-binary",
       "dash-editor-components",
       "python-dotenv"
   ],
)