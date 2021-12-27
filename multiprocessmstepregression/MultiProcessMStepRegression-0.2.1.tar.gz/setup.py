import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MultiProcessMStepRegression",
    version="0.2.1",
    author="王文皓(wangwenhao)",
    author_email="DATA-OG@139.com",
    description="python多进程逐步回归。python step-wise regression with multi-processing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wangwenhao-DATA-OG/MultiProcessMStepRegression",
    packages=setuptools.find_packages(),
    install_requires = ['scikit-learn>=0.20.4','statsmodels>=0.10.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)