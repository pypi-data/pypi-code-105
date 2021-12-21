from setuptools import setup, find_packages

setup(
   name='simple-component-folder', 
   version='0.0.1',
   description='A useful slider module',
#   py_modules=['setup.py','main_program', 'simplecomponent'], 
   author='Siamese',
   author_email='null@null.com',
   license='MIT',
 
   packages=find_packages('simple-component-folder'),
   package_dir={'': 'simple-component-folder'},  
   install_requires=['ipython==7.30.1', 'streamlit==1.2.0', ] 
   )
#'numpy==1.14.5', 'python_version>="0.0.2'