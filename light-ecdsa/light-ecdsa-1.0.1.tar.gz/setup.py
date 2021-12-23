from setuptools import setup, find_packages

VERSION = "1.0.1"
DESCRIPTION = "Minimalistic ecdsa"

setup(
    name="light-ecdsa",
    version=VERSION,
    author="0xFrijolito",
    author_email="<dante_torobolino@protonmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=["python", "ecdsa", "signatures"],
    classifies=[
        "Development :: 1 - Planning",
        "Intented Audience :: Developers",
        "Programming Lenguage :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)
