from setuptools import setup, find_packages

setup(
    name="pg_to_evalscript",
    version="0.0.4",
    packages=["pg_to_evalscript"],
    package_data={"pg_to_evalscript": ["javascript_datacube/*.js", "javascript_processes/*.js"]},
)
