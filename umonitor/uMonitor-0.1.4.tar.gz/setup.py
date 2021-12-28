# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['umonitor']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'umonitor',
    'version': '0.1.4',
    'description': 'A package to run and monitor background services',
    'long_description': '# uMonitor\n\nThis is a minimalistic python supervisor for your \nmicroservices.  \nOnce started, it will launch all the services you\'ve specified \nin the provided config file, and monitor their execution.\nSuppose you have following services in the `config.json`:\n```json\n{\n    "services" : [\n        {\n            "comment": "Another service to run and monitor.",\n            "program" : "python3",\n            "args" : ["other_script.py"],\n            "persist"  : true,\n            "cwd" : "/opt"\n        },\n        {\n            "comment": "And this one should not be restarted",\n            "program" : "bash",\n            "args" : ["will_be_executed_with_bin_bash.sh"],\n            "persist" : false,\n            "cwd" : "/opt"\n        }\n    ]\n}\n```\nThen the supervisor (uMonitor) will run the specified commands\nand for those which have `persis` set, will restart the described\nprocesses, whenever they fail/crash.\n\nMore complex: it also provides environment variables and venv-like\nbehavior for the specified programs. See the `config_example.json`\nfor more details.\n\n```json{\n    "comment": "Treat this as virtual environment, but not only for python.",\n    "interpreters" : {\n        "python3" : "/venv_some/bin/python3",\n        "sh" : "/bin/sh",\n        "bash" : "/bin/bash"\n    },\n\n    "comment": "Services to run and monitor.",\n    "services" : [\n        {\n            "program" : "python3",\n            "args" : ["script_1.py"],\n            "comment": "Do not recover after crashes",\n            "persist" : false,\n            "cwd" : "/opt",\n            "env" : {\n                "PYTHONPATH" : [\n                    "/opt/your_python_module/",\n                    "/usr/local/another/module/",\n                    "/joined_with/colon/will_be"\n                ],\n                "PATH": [\n                    "/opt/prog_1/bin/",\n                    "/home/username/.prog_2/bin/",\n                    "/joined_with/colon/will_be"\n                ],\n                "ENVIRON_VARIABLE": [\n                    "SINGLE_VALUE_42"\n                ]\n            }\n        },\n        {\n            "comment": "Another service to run and monitor.",\n            "program" : "python3",\n            "args" : ["other_script.py"],\n            "persist"  : true,\n            "cwd" : "/opt"\n        },\n        {\n            "comment": "And this one should not be restarted",\n            "program" : "bash",\n            "args" : ["will_be_executed_with_bin_bash.sh"],\n            "persist" : false,\n            "cwd" : "/opt"\n        }\n    ]\n}\n```\n',
    'author': 'Ruslan Sergeev',
    'author_email': 'mybox.sergeev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RuslanSergeev/uMonitor.git',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
