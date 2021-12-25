from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='binancetrader',
    version='0.0.1',
    author='Amir Ayat',
    author_email='amirayat20@gmail.com',
    description='It is a client-side package of Jirnals trading system as a Binance REST Api-based SDK midleware. Valid Binance account and Jirnal account are required to work with this package.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
