import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pygwbl',
    version='1.1',
    py_modules=['pygwbl'],  # 这个要跟发布的模块名一致
    author='Dagwbl',
    author_email='Dagwbl@qq.com',
    url='https://github.com/Dagwbl/pygwbl',
    project_urls={
        "Bug Tracker": "https://github.com/Dagwbl/pygwbl/issues",
    },
    description='这是我的第一个发布',
    long_description="Dagwbl's personal tool set. ",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
    )
