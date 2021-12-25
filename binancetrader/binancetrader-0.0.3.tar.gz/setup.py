import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="binancetrader",
    version="0.0.3",
    author="Amir Ayat",
    author_email="amirayat20@gmail.com",
    description='It is a client-side package of Jirnals trading system as a Binance REST Api-based SDK midleware. Valid Binance account and Jirnal account are required to work with this package.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Jirnal": "https://jirnal.ir/",
    },
    install_requires=[    
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
