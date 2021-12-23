from distutils.core import setup
setup(
  name = 'sessionOffedul',         # How you named your package folder (MyLib)
  packages = ['sessionOffedul'],   # Chose the same as "name"
  version = '0.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This package supports flask and it is easy to use, it has the main scope to make Flask Session Managment more easy and customizable!',   # Give a short description about your library
  author = 'OffedulDev',                   # Type in your name
  author_email = 'aloneforever.commercial@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/OffedulDev/session',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/OffedulDev/session/archive/refs/tags/v_03.tar.gz',    # I explain this later on
  keywords = ['HELPFUL', 'EASY', 'CUSTOMIZABLE', 'FLASK'],   # Keywords that define your package best
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
)
