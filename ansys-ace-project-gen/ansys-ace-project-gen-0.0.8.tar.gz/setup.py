from setuptools import setup, find_packages

CLASSIFIERS = [
    "Development Status :: 1 - Planning",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
]

setup(name='ansys-ace-project-gen',
      version='0.0.8',
      url='',
      license='GNU-GPL',
      author='Babacar FALL',
      author_email='babacar.fall@ansys.com',
      entry_points={"console_scripts": ["ansys-ace-project-gen = createaceproject.main:cli"]},
      description='Ansys ACE Project Generator',
      keywords=['python', 'ansys', 'ace'],
      packages=find_packages(),
      install_requires=['easygui'],
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      include_package_data=True,
      package_data={'createaceproject.templates': ['../*']},
      zip_safe=False,
      classifiers=CLASSIFIERS,
 )