import setuptools
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="easygoogletranslate",  
    version="0.0.1",
    author="Ahmet Eren Odacı",
    author_email="ahmetererenodaci@gmail.com",
    description="Easy Google Translate",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ahmeterenodaci/easygoogletranslate",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5.5',
    install_requires=["requests>=2.26.0"]
)