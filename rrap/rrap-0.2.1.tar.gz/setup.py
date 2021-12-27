from setuptools import setup

setup(name='rrap',
      version='0.2.1',
      description='A metagenomic read recruitment data pipeline',
      url='https://github.com/Kojiconner/rrap_metag_pkg/',
      author='Conner Kojima',
      author_email='cykojima@usc.edu',
      license='MIT',
      packages=['rrap'],
      install_requires=[
        "matplotlib>=3.0.3,<3.1",
        "numpy>=1.19.1,<1.20",
        "joblib>=0.16.0,<0.16.2",
        "scikit-learn>=0.23.1,<0.23.2",
	"pandas>=0.24.2,<0.24.3",
        "scipy>=1.5.2,<1.5.3",
        "threadpoolctl>=2.1.0,<2.1.1"
      ],
      python_requires=">=3.7.3",
      package_dir={"": "src"},
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      zip_safe=False)
