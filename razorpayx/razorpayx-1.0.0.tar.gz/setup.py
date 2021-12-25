from setuptools import setup

with open('README.md') as readme:
    readme_content = readme.read()

setup(
    name="razorpayx",
    version="1.0.0",
    description="RazorpayX Python Client",
    long_description=readme_content,
    long_description_content_type='text/markdown',
    url="https://github.com/vishwamshuklaRazorpay/razorpayx-python",
    author="Team Razorpay",
    license="MIT",
    install_requires=["requests"],
    include_package_data=True,
    package_dir={'razorpayx': 'razorpayx', 'razorpayx.resources': 'razorpayx/resources'},
    packages=['razorpayx', 'razorpayx.resources'],
    keywords='RazorpayX',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",

        # List of supported Python versions
        # Make sure that this is reflected in .travis.yml as well
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',

        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
