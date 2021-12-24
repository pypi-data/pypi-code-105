import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "nqgcs",
    version = "0.1.4",
    url = 'https://bitbucket.org/luca_de_alfaro/nqgcs',
    license = 'BSD',
    author = 'Luca de Alfaro',
    author_email = 'luca@dealfaro.com',
    maintainer = 'Luca de Alfaro',
    maintainer_email = 'luca@dealfaro.com',
    description = 'Interface to Google Cloud Storage',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = ['nqgcs'],
    install_requires=[
        "google-cloud-storage",
        "google-auth",
    ],
    zip_safe = False,
    platforms = 'any',
    python_requires=">=3.7",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
