import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-spa-deploy",
    "version": "2.0.0.a1",
    "description": "This is an AWS CDK Construct to make deploying a single page website (Angular/React/Vue) to AWS S3 behind SSL/Cloudfront as easy as 5 lines of code.",
    "license": "MIT",
    "url": "https://github.com/nideveloper/CDK-SPA-Deploy.git",
    "long_description_content_type": "text/markdown",
    "author": "hi@cdkpatterns.com",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/nideveloper/CDK-SPA-Deploy.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "spa_deploy",
        "spa_deploy._jsii"
    ],
    "package_data": {
        "spa_deploy._jsii": [
            "cdk-spa-deploy@2.0.0-alpha.1.jsii.tgz"
        ],
        "spa_deploy": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk-lib>=2.2.0, <3.0.0",
        "constructs>=10.0.13, <11.0.0",
        "jsii>=1.48.0, <2.0.0",
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
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
