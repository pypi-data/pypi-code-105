import setuptools
from pathlib import Path

setuptools.setup(
    name="MehrdadPDF",
    version=2.0,
    long_description=Path(r'C:\\users\vomino.ir\hello\Mehrdadpdf\README.md').read_text(),
    packages=setuptools.find_packages(exclude=['test','data'])
)
