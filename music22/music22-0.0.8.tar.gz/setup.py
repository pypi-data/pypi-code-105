from setuptools import setup
import music22

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='music22',
      version = music22.__version__ ,
      description = 'A tool for musicological analysis from audio files. Now it is focused on modal music analysis : Scale analysis, tonic detection',
      long_description = readme(),
      classifiers = [
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
      ],
      keywords = 'musicology analysis from non-symbolic data',
      url = 'https://gitlab.com/AnasGhrab/music22',
      author = 'Anas Ghrab',
      author_email = 'anas.ghrab@gmail.com',
      license = 'GNU',
      python_requires=">=3.6",
      packages = ['music22',
		],
      install_requires = [
          'numpy','matplotlib','scipy','pandas','essentia','librosa'
      ],
      zip_safe=False)
