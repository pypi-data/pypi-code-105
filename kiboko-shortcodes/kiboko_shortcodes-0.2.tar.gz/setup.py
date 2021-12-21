from setuptools import setup, find_packages

VERSION = '0.2' 
DESCRIPTION = 'Python Shorcodes'
LONG_DESCRIPTION = 'Create and use WordPress-style shortcodes in your Python based app.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="kiboko_shortcodes", 
        version=VERSION,
        author="Bob Handzhiev",
        author_email="<handzhiev@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'shortcodes'],
        classifiers= [
            "Development Status :: 4 - Beta",            
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
    			"Operating System :: OS Independent",
        ]
)