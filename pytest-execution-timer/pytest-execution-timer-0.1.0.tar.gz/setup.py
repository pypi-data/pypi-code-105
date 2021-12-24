# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_execution_timer']

package_data = \
{'': ['*']}

entry_points = \
{'pytest11': ['execution_timer = pytest_execution_timer.plugin']}

setup_kwargs = {
    'name': 'pytest-execution-timer',
    'version': '0.1.0',
    'description': "A timer for the phases of Pytest's execution.",
    'long_description': '# pytest-execution-timer\n\nA plugin to use with Pytest to measure execution time of tests.\n\nDistinctly different from the `--durations` option of pytest,\nthis plugin measures specific pytest startup/collection phases.\n\nLeverages `pytest` hooks to measure execution time of phases.\n\n---\n\n## Installation\n\nRequires:\n\n- Python 3.7 or later.\n- Pytest 6.2 or later.\n\nInstall the plugin with any approach for your project.\n\nSome examples:\n\n```shell\npip install pytest-execution-timer\n```\n\n```shell\npoetry add --dev pytest-execution-timer\n```\n\n```shell\npipenv install --dev pytest-execution-timer\n```\n\nOr add it to your `requirements.txt` file.\n\n## Usage\n\nEnable the plugin with the `--execution-timer` option when running `pytest`:\n\n```console\n$ pytest --execution-timer\n...\nDurations of pytest phases in seconds (min 100ms):\n0.662\tpytest_runtestloop\n```\n\nControl the threshold (default 100ms) by passing `--minimum-duration=<value in ms>`:\n\n```console\n$ pytest --execution-timer --minimum-duration=1000  # 1 second\n```\n\n## Understanding the output\n\nThe best ay to start is to compare the difference of the `pytest_runtestloop` duration\nand the overall duration of the test run. Example:\n\n```console\nDurations of pytest phases in seconds (min 100ms):\n0.666\tpytest_runtestloop\n====== 4 passed in 0.68s ======\n```\n\nIn this example, there\'s not much lost between the test run and the `pytest_runtestloop`\nmeaning that the startup and collection phases are not taking too much time.\n\nIf there\'s a larger difference in the timings,\nlook to other emitted phases to understand what\'s taking the most time.\n\nThese can then be examined directly,\nor use other tools like [profilers](https://docs.python.org/3/library/profile.html)\nor [import timings](https://docs.python.org/3/using/cmdline.html#cmdoption-X).\n\n## License\n\nDistributed under the terms of the MIT license,\n"pytest-execution-timer" is free and open source software.\nSee `LICENSE` for more information.\n',
    'author': 'Mike Fiedler',
    'author_email': 'miketheman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/pytest-execution-timer/',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
