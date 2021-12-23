from distutils.core import setup
setup(
  name = 'bubble_model',
  packages = ['bubble_model'],
  version = '0.1',
  license='MIT',
  description = "Simulation of taylor's bubble",
  author = 'Borja Garcia',
  author_email = 'borjagarmarpy@gmail.com',
  url = 'https://github.com/user/reponame',
  download_url = 'https://github.com/Borjapy/Taylor_Bubble/archive/refs/tags/v_01.tar.gz',
  keywords = ['Bubble', 'Taylor', 'Gas diffusion'],
  install_requires=[            # I get to this in a second
          'numpy',
          'sklearn',
      ],
  classifiers=[
    'Development Status :: 4 - Beta', # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ],
)
