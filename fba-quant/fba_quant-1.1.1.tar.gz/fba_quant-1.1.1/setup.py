"""
Copyright 2022 FBA Quant.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fba_quant",
    version="1.1.1",
    author="FBA Quant",
    author_email="fbaquant@gmail.com",
    description="FBA Quant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fbaquant/fba-quant",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "aenum",
        "backoff",
        "cachetools",
        "certifi",
        "dataclasses;python_version<'3.7'",
        "deprecation",
        "funcsigs",
        "inflection",
        "lmfit<=1.0.2",  
        "more_itertools",
        "msgpack",
        "nest-asyncio",
        "pandas<=1.2.4",
        "pydash",
        "python-dateutil>=2.7.0",
        "requests",
        "scipy>=1.2.0,<=1.6.0;python_version<'3.7'",
        "scipy>=1.2.0;python_version>'3.6'",
        "statsmodels>=0.11.1,<0.13.0",
        "tqdm",
        "typing;python_version<'3.7'",
        "websockets",
    ],
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License"
    ],
)
