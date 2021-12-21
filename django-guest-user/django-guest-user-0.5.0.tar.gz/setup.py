# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['guest_user',
 'guest_user.contrib.allauth',
 'guest_user.management',
 'guest_user.management.commands',
 'guest_user.migrations',
 'guest_user.templatetags']

package_data = \
{'': ['*'], 'guest_user': ['templates/guest_user/*']}

setup_kwargs = {
    'name': 'django-guest-user',
    'version': '0.5.0',
    'description': 'A Django app that lets visitors interact with your site without registration.',
    'long_description': '[![Code Lint](https://github.com/julianwachholz/django-guest-user/actions/workflows/lint.yml/badge.svg)](https://github.com/julianwachholz/django-guest-user/actions/workflows/lint.yml)\n[![Python Tests](https://github.com/julianwachholz/django-guest-user/actions/workflows/test.yml/badge.svg)](https://github.com/julianwachholz/django-guest-user/actions/workflows/test.yml)\n[![Documentation](https://readthedocs.org/projects/django-guest-user/badge/?style=flat)](https://django-guest-user.readthedocs.io)\n\n# django-guest-user\n\nAllow visitors to interact with your site like a temporary user ("guest")\nwithout requiring registration.\n\nAnonymous visitors who request a decorated page get a real temporary user object\nassigned and are logged in automatically. They can use the site like a normal\nuser until they decide to convert to a real user account to save their data.\n\nInspired by and as an alternative for [django-lazysignup](https://github.com/danfairs/django-lazysignup)\nand rewritten for Django 3.1+ and Python 3.7+.\n\n## Documentation\n\nFind the [**complete documentation**](https://django-guest-user.readthedocs.io/)\non Read the Docs.\n\n## Quickstart\n\n1. Install the `django-guest-user` package from PyPI\n2. Add `guest_user` to your `INSTALLED_APPS` and migrate your database\n3. Add `guest_user.backends.GuestBackend` to your `AUTHENTICATION_BACKENDS`\n4. Include `guest_user.urls` in your URLs\n5. Decorate your views with `@allow_guest_user`:\n\n   ```python\n   from guest_user.decorators import allow_guest_user\n\n   @allow_guest_user\n   def my_view(request):\n       assert request.user.is_authenticated\n       return render(request, "my_view.html")\n   ```\n\nA more detailed guide is available in the\n[installation documentation](https://django-guest-user.readthedocs.io/en/latest/setup.html#how-to-install).\n\n## Contributing\n\nAll contributions are welcome! Please read the\n[contributing guidelines](CONTRIBUTING.md) in this repostory.\n\n## Development Status\n\nThis project is under active development. Thanks to\n[previous work](https://github.com/danfairs/django-lazysignup) the core\nfunctionality is well-established and this package builds on top of it.\n\nThis project was created because the original project has been in an inactive\nstate without major updates in a long time. The code base was rewritten with\nonly modern versions of Python and Django in mind.\n',
    'author': 'Julian Wachholz',
    'author_email': 'julian@wachholz.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/julianwachholz/django-guest-user',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
