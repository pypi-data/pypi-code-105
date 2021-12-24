import setuptools

version = '0.1.2'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='zenduty_airflow_operator',
    description='This Airflow plugin creates a Zenduty Alert when it is run.',
    version=version,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zenduty/zenduty_airflow_plugin",
    project_urls={
        "Bug Tracker": "https://github.com/Zenduty/zenduty_airflow_plugin/issues",
    },
    author='Nikhil Prem',
    author_email='nikhil@zenduty.com',
    license='MIT License',
    py_modules = ['zenduty_airflow_operator'],
    setup_requires=['setuptools', 'wheel'],
    install_requires=['zenduty-api'
                      ],
)