import setuptools

setuptools.setup(
    name="ecoforest",
    version="0.0.2",
    author="",
    author_email="",
    description="",
    long_description="an interpretable data-driven macroeconomic forecasting method based on N-BEATS neural network",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'hyperopt==0.2.5',
        'matplotlib==3.3.3',
        'numpy==1.18.5',
        'pandas==1.1.5',
        'requests==2.25.1',
        'scipy==1.4.1',
        'statsmodels==0.12.2',
        'torch==1.8.1+cpu',
        'tqdm==4.54.1',
    ],
)
