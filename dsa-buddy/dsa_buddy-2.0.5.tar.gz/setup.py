from setuptools import setup, find_packages

# reading long description from file
long_description = "DSA buddy client\n@Copyright 2021-22 [Botoservices]"


# specify requirements of your package here
REQUIREMENTS = ['requests']

# some more details
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    ]

# calling the setup function 
setup(name='dsa_buddy',
      version='2.0.5',
      description='dsa_buddy client for DSA preparation and code submission utlity',
      long_description=long_description,
      url='',
      author='Botoservices',
      author_email='botoservices@gmail.com',
      license='MIT',
      packages = find_packages(),
      entry_points ={
            'console_scripts': [
                'dsa_buddy=submit.submit:main'
            ]
    },
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='dsa buddy coding python'
      )
