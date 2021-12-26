from distutils.core import setup
setup(
  name = 'seamester',      
  packages = ['seamester'],
  version = '1.2',      
  license='MIT',       
  description = '',   
  author = 'PROgramJEDI',                   
  url = 'https://github.com/PROgramJEDI/seamester',   
  download_url = 'https://github.com/PROgramJEDI/seamester/archive/refs/tags/1.2.tar.gz', 
  keywords = ['courses', 'semester', 'degree', 'university', 'learn'],   
  install_requires=[     
          'sqlalchemy',
      ],
  classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
  ],
)