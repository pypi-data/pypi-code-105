from setuptools import setup, find_packages

DESCRIPTION = 'Financial Modeling Prep Wrapper and Quant Package'
LONG_DESCRIPTION = 'Financial Modeling Prep Wrapper and Quant Package'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="fmp_quant", 
        version='0.0.5',
        author="Francisco Ruiz",
        author_email="<franciscruiz11219@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pandas','numpy','requests'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'finance','quantitative finance','wrapper','financial modelling prep',
        'financial algorithm'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)