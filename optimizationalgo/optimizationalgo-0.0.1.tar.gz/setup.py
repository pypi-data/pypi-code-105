import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="optimizationalgo",
    packages=['optimizationalgo'],
    version="0.0.1",
    description='Ant simulation and simulated annealing algorithm',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mark Kozlov",
    author_email="mark.k.2012@yandex.ru",
    url="https://github.com/SMALA-comand/Optimization_algo",
)
