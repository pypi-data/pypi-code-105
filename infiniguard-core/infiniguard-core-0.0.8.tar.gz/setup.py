
SETUP_INFO = dict(
    name = 'infiniguard-core',
    version = '0.0.8',
    author = 'Maxim Kigel',
    author_email = 'mkigel@infinidat.com',

    url = None,
    license = 'BSD',
    description = """InfiniGuard Core Utils""",
    long_description = """InfiniGuard Core Utils for the Different InfiniGuard Projects""",

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = [
'colorama',
'infi.caching',
'requests',
'setuptools',
'infinisdk',
'fabric2'
],
    namespace_packages = [],

    package_dir = {'': 'src'},
    package_data = {'': []},
    include_package_data = True,
    zip_safe = False,

    entry_points = dict(
        console_scripts = [],
        gui_scripts = [],
        ),
)

if SETUP_INFO['url'] is None:
    _ = SETUP_INFO.pop('url')

def setup():
    from setuptools import setup as _setup
    from setuptools import find_packages
    SETUP_INFO['packages'] = find_packages('src')
    _setup(**SETUP_INFO)

if __name__ == '__main__':
    setup()

