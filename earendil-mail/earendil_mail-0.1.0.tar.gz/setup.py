# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['earendil']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.3.6,<4.0.0']

setup_kwargs = {
    'name': 'earendil-mail',
    'version': '0.1.0',
    'description': 'A Markdown-based HTML email API.',
    'long_description': '# Eärendil\n\nEärendil is a Markdown-based HTML email API written in Python. It allows users to draft an email message in Markdown \nand send it as a rich email viewable as both HTML and plaintext.\n\nMy primary motivation for creating this library was the lack of good options for sending rich emails with an alternative\nplaintext message for recipients who may be using a dated email service. I think that providing a faithful \nalternative message is important, and that simply using the Markdown used to generate the HTML message as the \nalternative is insufficient. Markdown, while fairly human-readable compared to most markup languages, still contains \nredundant or unhelpful syntax that is better expressed differently in plaintext. For example, escape characters \nshould be removed, as should heading and emphasis symbols.\n\n## Features\n\n* Renders Common Markdown messages into HTML.\n* Renders a subset of Markdown into plaintext.\n* Sends Markdown emails from either strings or files.\n\n### Planned Features\n\n* Bulk mailing functionality.\n* Support for rendering a greater subset of Markdown as plaintext.\n* Support for attachments.\n\n## Usage\n\nTo send Markdown-formatted emails using Eärendil, use either the `send_markdown_email`or `send_markdown_email_from_file`\nfunctions. Here is an example that uses each:\n\n```python\nfrom pathlib import Path\nfrom smtplib import SMTP\n\nfrom earendil import send_markdown_email, send_markdown_email_from_file\n\nsender_email = "sender@gmail.com"\npassword = "password"\nrecipient = "receiver@example.com"\n\nsubject = "Example Subject"\nmessage_path = Path("/path/to/markdown.md")\nwith message_path.open("r") as file:\n    message = file.read()\n\nwith SMTP("smtp.gmail.com", 587) as server:\n    server.starttls()\n    server.login(sender_email, password)\n    # Here, you can either use:\n    send_markdown_email(server, sender_email, recipient, subject, message)\n    # or, alternatively:\n    send_markdown_email_from_file(server, sender_email, recipient, subject, message_path)\n```\n\n## Installation\n\n### Requirements\n\nEärendil can run on any version of Python since `3.6.2` (inclusive). It also depends on the `markdown` library.\n\n### From PyPI\n\nThe easiest way to install Eärendil is to simply run the command `pip3 install earendil-mail`.\n\n### From Source\n\nAlternatively, Eärendil can be installed from source by cloning this repository. To do so, run the following commands:\n```commandline\ngit clone https://github.com/ADSteele916/earendil\ncd earendil\npip3 install .\n```\n\n## Uninstallation\n\nTo uninstall, simply run the command `pip3 uninstall earendil-mail`\n',
    'author': 'Alex Steele',
    'author_email': '45648397+ADSteele916@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ADSteele916/earendil',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
