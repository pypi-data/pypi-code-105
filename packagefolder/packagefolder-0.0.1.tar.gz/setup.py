from setuptools import setup, find_packages

setup(
   name='packagefolder', 
   version='0.0.1',
   description='A useful slider module',
#   py_modules=['setup.py','main_program', 'simplecomponent'], 
   author='Siamese',
   author_email='null@null.com',
   license='MIT',
   classifiers=[ 
        "License :: OSI Approved :: MIT License", 
        "Programming Language :: Python :: 3", 
        "Programming Language :: Python :: 3.7", 
   ],
   packages=["packagefolder"], 
   includepackagedata=True, 
 

  ## packages=find_packages('simple-component-folder'),
  # package_dir={'': 'simple-component-folder'},  
   install_requires=['ipython==7.30.1', 'streamlit==1.2.0'], 
   entrypoints={ 
       "console_scripts":[ 
           "src.packagefolder.__main__:main", 
       ] 
     }, 
   )
#'numpy==1.14.5', 'python_version>="0.0.2' /Users/theodorewarren/Documents/projectrelated/streaml/simplecomponenttwo/streamlit-env/dist/