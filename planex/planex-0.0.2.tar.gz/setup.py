import setuptools

setuptools.setup(
    name="planex",                     # This is the name of the package
    version="0.0.2",                        # The initial release version
    author="José Valencia Figueroa",                     # Full name of the author
    author_email="joel.jvalencia@gmail.com",
    description="Modulo que guarda la base de la prestaciones de los participes de un plan de pensiones de prestacion definida. USELESS",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    keywords=['insurance', 'actuarial science', 'life insurance', 'pension',
                'python', 'spain', 'life contingencies'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    install_requires=['pandas>=0.25.3',
                      'numpy>=1.17.4'])   # Install other dependencies if any
