import setuptools
with open(r'C:\Users\bigsmall\Desktop\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='slovik',
	version='1.0',
	author='Chelik',
	author_email='kto9228322@gmail.com',
	description='EZ',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=['slovik'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)