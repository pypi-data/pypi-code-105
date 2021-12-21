import re
import setuptools


def find_version(version_file_path):
    with open(version_file_path) as version_file:
        version_match = re.search(r"^__version_tuple__ = (.*)", version_file.read(), re.M)
        if version_match:
            ver_tup = eval(version_match.group(1))
            ver_str = ".".join([str(x) for x in ver_tup])
            return ver_str
        raise RuntimeError("Unable to find version tuple.")

if __name__ == "__main__":
    setuptools.setup(
        name="packagedeployer",
        version=find_version("packagedeployer/version.py"),
        include_package_data=True,
        setup_requires=["ninja"],  # ninja is required to build extensions
        packages=setuptools.find_packages(exclude=("tests", "tests.*")),
    )
