from distutils.core import setup
setup(
  name = 'get-random-wallet-info',         
  packages = ['get-random-wallet-info'],   
  version = '0.1',     
  license='MIT',       
  description = 'CHECKS RANDOM WALLETS USING SEED.',   
  author = 'truewill06',                   
  author_email = 'truewill06@gmail.com',      
  url = 'https://github.com/truewill06/get-random-wallet-info',  
  download_url = 'https://github.com/truewill06/check-random-wallet/archive/refs/tags/0.1.tar.gz',    
  keywords = ['BITCOIN', 'SEED'],   
  install_requires=[            
          
          
	  'bip32utils',
	  'bs4',
          
	  
          
	
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.10',
  ],
)
