import setuptools


setuptools.setup(
    name="Evison",
    version="0.4",
    author="Jones Lin",
    author_email="jonneslin@gmail.com",
    description="Feature map visualization",
    url="https://github.com/JonnesLin/Evison",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'torchviz'
    ]
)