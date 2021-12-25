from setuptools import setup

with open('README.md') as readme:
    readme_content = readme.read()

setup(
    name="vishwam_test",
    version="1.0",
    description="squares the number",
    long_description=readme_content,
    long_description_content_type='text/markdown',
    url="https://github.com/vishwamshuklaRazorpay/vishwam_test",
    author="Vishwam",
    license="MIT",
    classifiers=[
            "License :: OSI Approved :: MIT License",
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ],
    packages=["square"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts":[
            "square=square.main:main",
        ]
    },
)
