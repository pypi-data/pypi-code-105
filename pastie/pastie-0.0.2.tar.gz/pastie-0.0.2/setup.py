from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'A simple interaction tool for the pastie.io API.'
LONG_DESCRIPTION = 'The unofficial interaction tool for pastie.io\'s pastebin-like API.\n## Use:\n```py\nfrom pastie import pastie\nx = pastie.Paste("FooBar")\nprint(x)```'

# Setting up
setup(
       # the name must match the folder name
        name="pastie", 
        version=VERSION,
        author="1305",
        author_email="outsider.1305@outlook.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'API', 'wrapper', 'http', 'requests'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ]
)
