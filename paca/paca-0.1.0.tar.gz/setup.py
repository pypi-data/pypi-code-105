import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="paca",
    version="0.1.0",
    author="Robert Gomez, Jr.",
    author_email="rgomezjnr@gmail.com",
    description="Check asset status using Alpaca Broker API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rgomezjnr/paca",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=["alpaca_trade_api", "colorama"],
    license="MIT",
    entry_points ={'console_scripts':['paca=paca.paca:run']},
    keywords="alpaca broker api asset stock market crypto trading finace investment python cli tool script",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Financial and Insurance Industry",
        "Natural Language :: English",
        "Topic :: Internet",
        "Topic :: Utilities",
        "Topic :: Office/Business :: Financial :: Investment"
    ]
)