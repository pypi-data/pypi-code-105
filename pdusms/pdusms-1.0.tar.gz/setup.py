import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name = "pdusms",
    version = "1.0",
    description = "PDU Converter: SMS PDU encoding and decoding, including GSM-0338 character set, support Python 3",
    long_description = long_description,
    long_description_content_type="text/markdown",
    author = "Tran Tu Quang",
    author_email = "tuquangtran123@gmail.com",
    url = 'http://pypi.python.org/pypi/smspdu',
    classifiers = [
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: BSD License',
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)

# vim: set filetype=python ts=4 sw=4 et si
