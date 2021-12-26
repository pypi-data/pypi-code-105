from setuptools import setup, find_packages

requirements = [
    "httpx[all]",
    "typing",
    "websockets", 
    "ujson"
]

setup(name = "pyanon",
      version = "1.0",
      description = "Api for new anonym client",
      packages = find_packages(),
      author_email = "ktoya170214@gmail.com",
      install_requires = requirements,
      zip_safe = False)