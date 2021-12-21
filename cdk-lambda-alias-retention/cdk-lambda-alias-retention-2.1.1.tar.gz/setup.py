import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-lambda-alias-retention",
    "version": "2.1.1",
    "description": "cdk-lambda-alias-retention",
    "license": "Apache-2.0",
    "url": "https://github.com/kimisme9386/cdk-lambda-alias-retention.git",
    "long_description_content_type": "text/markdown",
    "author": "Chris Yang<kimisme9386@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/kimisme9386/cdk-lambda-alias-retention.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_lambda_alias_retention",
        "cdk_lambda_alias_retention._jsii"
    ],
    "package_data": {
        "cdk_lambda_alias_retention._jsii": [
            "cdk-lambda-alias-retention@2.1.1.jsii.tgz"
        ],
        "cdk_lambda_alias_retention": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk-lib>=2.1.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.49.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
