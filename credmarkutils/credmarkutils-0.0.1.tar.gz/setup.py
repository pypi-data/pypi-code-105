from setuptools import setup

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
		name='credmarkutils',
		version='0.0.1',
		description='Credmark Utils',
		py_modules=["helloworld"],
		package_dir={'':'src'},
		classifier=[
			"Programming Language :: Python ::3",
			"Programming Language :: Python :: 3.6",
			"License :: OSI Approved :: GNU General Public License v3.0",
			"Operating System :: OS Independent",
		],
		long_description=long_description,
		long_description_content_type="text/markdown",
		install_requires = [

		],
		extras_require = {
			"dev":[
				"pytest>=3.7",
			],
		},
		url="https://github.com/credmark/credmarkutils",
		author="Nishchal Gaba",
		author_email="nishchal@credmark.com",
	)