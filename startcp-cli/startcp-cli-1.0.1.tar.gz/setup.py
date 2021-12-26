import setuptools
import subprocess
import os


startcp_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)
assert "." in startcp_version

assert os.path.isfile("startcp/version.py")
with open("startcp/VERSION", "w", encoding="utf-8") as fh:
    fh.write(f"{startcp_version}\n")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="startcp-cli",
    version=startcp_version,
    author="Sujit and Ankush",
    author_email="ankushpatil6174@gmail.com",
    description="A CLI boiler plate for current competition.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asprazz/startcp-cli",
    packages=setuptools.find_packages(),
    package_data={"startcp-cli": ["VERSION"]},
    include_package_data=True,
    python_requires=">=3.6",
    entry_points={
            'console_scripts': [
                'startcp=startcp.__main__:main'
            ]
    },
    install_requires=[
        'requests>=2.23',
        'argparse',
        'colorama',
        'python-dotenv',
        'Rangebi'
    ],
)
