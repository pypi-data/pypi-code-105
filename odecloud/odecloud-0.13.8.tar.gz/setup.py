# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odecloud', 'odecloud.api']

package_data = \
{'': ['*']}

install_requires = \
['certifi==2021.10.8',
 'charset-normalizer==2.0.9',
 'idna==3.3',
 'requests==2.26.0',
 'urllib3==1.26.7']

setup_kwargs = {
    'name': 'odecloud',
    'version': '0.13.8',
    'description': 'Python client for https://server.odecloud.app',
    'long_description': "# Official OdeServer Python API's Client\n\n## Getting Started & Usage\n\n1. Installation:\n\n- Use Poetry:\n    ```sh\n    $ poetry add odecloud\n    ```\n- Or, use Pip:\n    ```sh\n    $ pip install odecloud\n    ```\n\n2. Instantiate your connection to OdeCloud's API:\n\n- If you don't know your client credentials:\n    ```py\n    api = Api('https://server.odecloud.app/api/v1') # All API calls will be made to this domain.\n    api.login('your-email@here.com', 'your_password')\n    ```\n\n- If you already know your client credentials:<br>\n    ```py\n    api = Api(\n        base_url='https://server.odecloud.app/api/v1', # All API calls will be made to this domain\n        client_key='YOUR CLIENT KEY',\n        client_secret='YOUR CLIENT SECRET',\n    )\n    ```\n\n3. Now, any calls can be made to OdeCloud's API. Examples below:\n    ```py\n    api.comments.get(createdBy=random_user_id) # GET /api/v1/comments?createdBy=random_user_id/\n    api.comments.post(data=expected_payload) # POST /api/v1/comments/\n    api.comments(random_comment_id).patch(data=expected_payload) # PATCH /api/v1/comments/random_comment_id/\n    api.comments(random_comment_id).delete() # DELETE /api/v1/comments/random_comment_id/\n    ```\nHappy coding!\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)",
    'author': 'Vanielle',
    'author_email': 'vanielle@odecloud.com',
    'maintainer': 'OdeCloud',
    'maintainer_email': 'support@odecloud.com',
    'url': 'https://gitlab.com/odetech/python_odecloud',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
