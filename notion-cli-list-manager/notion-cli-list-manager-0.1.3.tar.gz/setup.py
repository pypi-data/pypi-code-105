# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notion_cli_list_manager']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0',
 'prettytable>=2.5.0,<3.0.0',
 'requests>=2.26.0,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['list = notion_cli_list_manager.main:app']}

setup_kwargs = {
    'name': 'notion-cli-list-manager',
    'version': '0.1.3',
    'description': 'A simple line-command tool for managing Notion List Databases.',
    'long_description': '\n#### ⚠️ This project is still in work in progress. Commands could change in the future.\n\n\n# Notion CLI List Manager 🗂\n### Increase your productivity with a simple command. 🛋\n\nA simple command-line tool for managing [Notion](http://notion.so) ___List___ databases. ✨ You can copy [my free simple template](https://jacksalici.notion.site/d75c9590dc8b4d62a6c65cbf3fdd1dfb?v=0e3782222f014d7bb3e44a87376e3cfb).\n\n## 📺 Features:\n- fast and simple, saving your idea is as simple as digit `add "get money"` 💆\u200d♂️\n- tables are pretty printed with fab ascii tables 🌈\n- parameters are going to be supported 🎻\n\n\n## 🧰 Syntax:\n\n| Commands:|    | Args and options:|\n|---|---|---|\n| `list` | to display all the ___List___ not done yet. | `--db [id] ` to display a specific database. <br> `--all` to display all the lists.\n| `list add [title]` | to add a new ___List___ called `title`. |   `[title]` will be the text of the ___List___ (and the title of the associated Notion database page)  <br> `--db [id] ` to add the entry to a specific database. Otherwise, the default database will be used.| \n| `list rm [index]` | to remove the ___List___ with the index `index`.  <br> _(Command to call after `list all`)_| `[index]` has to be formatted either like a range and a list, or a combination of these. E.g.: 3,4,6:10:2 will remove pages 3, 4, 6, 8.\n| `list db` | to display all the notion display saved in the manager. | `--label [LABEL] --id [ID]` to add a database to the manager. <br> `--rm [LABEL]` to remove a database named [LABEL] from the manager. Note that adding or removing a database to the manager does not cause the actual creation or deletion on Notion.\n| `list set --token [token] --id [database_id]` | to set the token and the ID of the Notion Database you want as default. _This must be executed as the first command_. | You can get the `[token]` as internal api integration [here](https://www.notion.so/my-integrations). <br> You can get the database id from the database url: notion.so/[username]/`[database_id]`?v=[view_id].  | \n## 🔬 Usage:\n\nAlthough it is a beta version, the package is already downloadable from pypi.org yet.\n\n```\npip install notion-cli-list-manager\n```\n\nYou can also clone the repo to have always the very last version.\nHaving installed Python3 and Pip3 on your machine, write on the terminal:\n\n``` \n    git clone https://github.com/jacksalici/notion-cli-list-manager.git notion-cli-list-manager\n\n    pip3 install notion-cli-list-manager/dist/notion-cli-list-manager-0.1.*.tar.gz\n```\n\nThen set the token and the database id:\n\n```\n    list set --token [token] --id [database-id]\n``` \n_📌 Note that you must share the database with your integration!_  \nAnd finally, you can use the commands above.\n\n\n## 🛒 Still to do:\nSee the [project tab](https://github.com/jacksalici/notion-cli-list-manager/projects/1) for a complete and real-time-updated list.\n\n## 💌 Collaboration:\nIssues and PRs are really appreciated. \n\n\n    ',
    'author': 'Jack Salici',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
