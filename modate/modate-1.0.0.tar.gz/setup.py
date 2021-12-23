from setuptools import setup

setup(
    name='modate',
    version='1.0.0',    
    description='A python package to change "created", "modificated" or "last accessed" dates of a file.',
    url='https://github.com/dontic/modate',
    author='Daniel Garcia Sanchez',
    author_email='',
    license='LGPLv3+',
    packages=['modate'],
    install_requires=['click'],
    entry_points={
        'console_scripts': 
        ['modate=modate:main',
        ],
    },
    classifiers=[
        'Environment :: Console',
        'Natural Language :: English',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Desktop Environment :: File Managers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',      
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)