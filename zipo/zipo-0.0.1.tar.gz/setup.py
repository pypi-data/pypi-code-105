import setuptools

with open('README.md', 'r')as f:
    long_description = f.read()

setuptools.setup(
    name='zipo',
    version='0.0.1',
    author='xiongtianshuo',
    author_email='seoul1k@163.com',
    description='functions.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    maintainer='xiongtianshuo',
    maintainer_email='seoul1k@163.com',
    url='https://github.com/seoul2k/zipp',
    license='BSD License',
    packages=['zipo/'],
    platforms=["all"],
    project_urls={
        "Bug Tracker": "https://github.com/seoul2k/zipp/issues",
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=['zipfile']
)
