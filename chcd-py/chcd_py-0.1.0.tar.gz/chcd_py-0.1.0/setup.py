from setuptools import setup

setup(name='chcd_py',
      version='0.1.0',
      description="python modules for CHCD",
      url='https://github.com/datagarret-uth/chcd_py',
      author="Garret Munoz",
      author_email="datagarret@gmail.com",
      license='MIT',
      packages=['chcd_py'],
      install_requires=['pandas', 'psycopg-binary'])
