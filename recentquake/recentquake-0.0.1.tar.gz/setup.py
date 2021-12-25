import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="recentquake",
    version="0.0.1",
    author="toshiki miyagawa",
    author_email="s1922033@stu.musashino-u.ac.jp",
    description="A package for visualization of the characteristics of earthquakes in the last 30 days",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/miyagawa-toshiki/recentquake",
    project_urls={
        "Bug Tracker": "https://github.com/miyagawa-toshiki/recentquake",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['recentquake'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points = {
        'console_scripts': [
            'recentquake = recentquake:main'
        ]
    },
)
