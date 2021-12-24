from distutils.core import setup
setup(
  name = 'focus_tracker_test',         # How you named your package folder (MyLib)
  packages = ['focus_tracker_test'],   # Chose the same as "name"
  version = '0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'TEST',   # Give a short description about your library
  author = 'NIKHIL',                   # Type in your name
  author_email = 'mvsnikhil51@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/NIKHILMVS/focus-tracker',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/NIKHILMVS/focus-tracker',    # I explain this later on
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
    include_package_data=True,
    install_requires=['python-dateutil',
                      'plotly', "pywin32", 'uiautomation','easygui'],
    zip_safe=False,
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/NIKHILMVS/focus-tracker',
        'Source': 'https://github.com/NIKHILMVS/focus-tracker'
    },
    entry_points='''
        [console_scripts]
        apptracker=apptracker.__init__:main
        '''
)