from setuptools import setup
from pathlib import Path

this_dir = Path(__file__).parent
long_description = (this_dir / "README.md").read_text()


setup(
	name="lsl-cli", 
	version='0.1.0', 
	description="Command-line tools for the Lab Streaming Layer.",
	url="https://github.com/yop0/lsl-cli", 
	author="Johan Medrano",
	author_email="johan.medrano653@gmail.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
	license="MIT",
	entry_points = {
		'console_scripts': [
			'lsl=lsl_cli.lsl:main'
		]
	}, 
	packages=['lsl_cli'],
	install_requires = [
		'pylsl'
	],
	package_data = {
		'lsl_cli': ['extra/lsl-completion.*', 'extra/lsl_complete_script.sh']
	}, 
	classifiers = [
        'Development Status :: 1 - Planning',
	]
) 
