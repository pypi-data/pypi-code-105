# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tgpy', 'tgpy.handlers', 'tgpy.run_code']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'Telethon>=1.24.0,<2.0.0',
 'aiorun>=2021.10.1,<2022.0.0',
 'cryptg>=0.2.post4,<0.3',
 'pydantic>=1.8.2,<2.0.0',
 'rich>=10.16.1,<11.0.0']

entry_points = \
{'console_scripts': ['tgpy = tgpy.main:main']}

setup_kwargs = {
    'name': 'tgpy',
    'version': '0.2.0',
    'description': 'Run Python code right in your Telegram messages',
    'long_description': '![TGPy](https://raw.githubusercontent.com/tm-a-t/TGPy/master/readme_assets/TGPy.png)\n\n## Run Python code right in your Telegram messages\n\nMade with Telethon library, TGPy is a tool for evaluating expressions and Telegram API scripts.\n\n- Do Python calculations in dialogs\n- Interact with your messages and chats\n- Automate sending messages and more\n\n![Example](https://raw.githubusercontent.com/tm-a-t/TGPy/master/readme_assets/example.gif)\n\nJust send Python code to any chat, and it will be executed. Change your message to change the result.\n\n# Examples\n\nSend any of these examples to any chat to evaluate:\n\n🐍 Do Python calculations\n\n```python\nfor i in range(5):\n    print(i)\n```\n\n⏳ Delete the current message in 5 seconds\n\n```python\nimport asyncio\n\nawait asyncio.sleep(5)\nawait msg.delete()\n```\n\n↪️ Forward the message you replied to to another chat\n\n```python\norig.forward_to(\'Chat title\')\n```\n\n🖼 Send all chat profile photos to the same chat\n\n```python\nphotos = await client.get_profile_photos(msg.chat)\nmsg.reply(file=photos)\n```\n\n🔖 Define a function which forwards messages to Saved Messages with reply\n\n```python\ndef save():\n    message = ctx.msg\n    original = await message.get_reply_message()\n    await original.forward_to(\'me\')\n    return \'Saved!\'\n``` \n\n🗑 Define a function which deletes messages with reply\n\n```python\nasync def delete():\n    message = ctx.msg\n    original = await message.get_reply_message()\n    await original.delete()\n    await message.delete()\n```\n\n# Guide\n\n- [Basics](https://tgpy.tmat.me/basics/)\n- [TGPy builtins](https://tgpy.tmat.me/builtins/)\n- [Code detection](https://tgpy.tmat.me/code_detection/)\n\n# Installation\n\n1. You\'ll need Telegram API key. Register your "app" at [my.telegram.org](https://my.telegram.org) to get `api_id` and \n`api_hash`. App title and other data don\'t matter.\n\n2. Clone the repo:\n   ```shell\n   > git clone https://github.com/tm-a-t/TGPy\n   > cd TGPy\n   ```\n\n3. Create `config.py`. Enter your API data and your phone to log in:\n   ```python\n   api_id = ...\n   api_hash = ...\n   phone = ...\n   ```\n\n4. Install the requirements and run TGPy:\n   ```shell\n   > pip install -r requirements.txt\n   > python -m tgpy\n   ```\n\n5. For the first time, you\'ll need to log in with a confirmation code from Telegram.\n\nSend `ping()` to any chat to check if TGPy is running.\n\n# Credits\n\n- Thanks to [penn5](https://github.com/penn5) for [meval](https://github.com/penn5/meval)\n- Thanks to [Lonami](https://github.com/LonamiWebs) for [Telethon](https://github.com/LonamiWebs/Telethon)\n\n# License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'tmat',
    'author_email': 'a@tmat.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tm-a-t/TGPy/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
