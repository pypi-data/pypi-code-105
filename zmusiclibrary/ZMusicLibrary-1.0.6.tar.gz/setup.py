# from distutils.core import setup
import setuptools

f = open("README.md", "r", encoding="utf-8")
long_description = f.read()
print(long_description)
f.close()

setuptools.setup(
  name = 'ZMusicLibrary',         # How you named your package folder (MyLib)
  packages = ['ZMusicLibrary'],   # Chose the same as "name"
  version = '1.0.6',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'An extremely easy way to create notes, intervals, chords, and scales! Save yourself the trouble of music theory!',   # Give a short description about your library
  author = 'Zeyn Schweyk',                   # Type in your name
  author_email = 'zschweyk@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/ZSchweyk/MusicLibrary',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/ZSchweyk/ZMusicLibrary/archive/refs/tags/v1.0.6.tar.gz',    # I explain this later on
  keywords = ['notes', 'intervals', 'chords', 'scales', 'custom', 'pre-defined', 'music', 'piano'],   # Keywords that define your package best
  project_urls = {
    "Portfolio Description": "https://2022mechatronicszeynschweyk.weebly.com/senior_year_capstone",
  },
  install_requires=[],           # I get to this in a second
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    "Operating System :: OS Independent",
    'Programming Language :: Python :: 3',      #Specify which python versions that you want to support
  ],
  python_requires=">=3.6",
)