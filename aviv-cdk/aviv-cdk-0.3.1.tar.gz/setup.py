import setuptools
import aviv_cdk

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aviv-cdk",
    version=aviv_cdk.__version__,
    author="Jules Clement",
    author_email="jules.clement@aviv-group.com",
    description="Aviv CDK Python library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aviv-group/aviv-cdk-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    py_modules=[
        'bin.aws_local',
        'bin.sfn_extract'
    ],
    data_files=[
        ("share/aviv-cdk/cfn-resources", ["lambdas/cfn_resources/requirements.txt"])
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'aviv-aws=bin.aws_local:cli',
            'aviv-cdk-sfn-extract=bin.sfn_extract:cli'
        ],
    },
    install_requires=[
         "boto3>=1.20.26",
         "botocore>=1.23.26",
         "click>=8.0.1",
         "aws-cdk-lib>=2.3.0"
   ],
    setup_requires=['pytest-runner>=5.3.1'],
    tests_require=['pytest'],
    python_requires='>=3.8',
    use_2to3=False,
    zip_safe=False
)
