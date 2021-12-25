# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlit_cookies_manager']

package_data = \
{'': ['*'],
 'streamlit_cookies_manager': ['build/*',
                               'build/static/js/*',
                               'public/*',
                               'src/*']}

install_requires = \
['streamlit>0.63']

setup_kwargs = {
    'name': 'streamlit-cookies-manager',
    'version': '0.1.0',
    'description': 'Access and save cookies from Streamlit',
    'long_description': '# Streamlit Cookies Manager\n\nAccess and change browser cookies from Streamlit scripts:\n```python\nimport streamlit as st\nfrom streamlit_cookies_manager import CookieManager\n\n# This should be on top of your script\ncookies = CookieManager()\nif not cookies.ready():\n    # Wait for the component to load and send us current cookies.\n    st.stop()\n\nst.write("Current cookies:", cookies)\nvalue = st.text_input("New value for a cookie")\nif st.button("Change the cookie"):\n    cookies[\'a-cookie\'] = value  # This will get saved on next rerun\n    if st.button("No really, change it now"):\n        cookies.save()  # Force saving the cookies now, without a rerun\n```\n',
    'author': 'Tomasz Kontusz',
    'author_email': 'tomasz.kontusz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
