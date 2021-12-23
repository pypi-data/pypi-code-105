from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setup(
    name='zzsukitest',
    version='1.0.4',
    author='zzsuki',
    author_email='zzsuki@163.com',
    url='https://gitee.com/he_weidong/zzsuki_tests',
    description='test runner for automation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["Jinja2", "PyYAML", "requests==2.24.0"],
    packages=find_packages(),
    package_data={
        "": ["*.html", '*.md'],
    },
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
