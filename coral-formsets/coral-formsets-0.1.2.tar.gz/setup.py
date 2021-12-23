# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['coral_formsets', 'coral_formsets.templatetags']

package_data = \
{'': ['*'], 'coral_formsets': ['static/coral_formsets/js/*']}

install_requires = \
['Django>=2.2']

setup_kwargs = {
    'name': 'coral-formsets',
    'version': '0.1.2',
    'description': 'Coral formsets',
    'long_description': '# coral-formsets\n\nExtensão para manipular o frontend usando Django [FormSets](https://docs.djangoproject.com/en/dev/topics/forms/formsets/).\n\nNão tem dependência com outro framework/biblioteca javascript.\n\n## Documentation\n\n### Installation\n\nPara instalar coral-formsets:\n\n```shell\npip install coral-formsets\n```\n\nAdicione `coral_formsets` em `INSTALLED_APPS`:\n\n```python\nINSTALLED_APPS = [\n    # other apps\n    "coral_formsets",\n]\n```\n\n### Usage\n\nNo seu html adicione o `js` como no exemplo abaixo.  \nNesse exeplo `yourapp/form.html` é um arquivo referente ao template do seu form, isso garante mais clareza ao seu código:\n\n```html\n<!-- yourapp/form.html -->\n<div data-form>\n  <div style="display: none">{{ form.DELETE }}{{ form.id }}</div>\n  {{ form.as_p }}\n  <button data-delete>\n    delete form\n  </button>\n</div>\n```\n\n```html\n<!-- yourapp/view.html -->\n{% load static coral_formset_tags %}\n<!DOCTYPE html>\n<html>\n<body>\n  <div data-formset>\n    {% render_empty_form_template \'yourapp/form.html\' formset as empty_form %}\n\n    {{ formset.management_form }}\n\n    <div data-body>\n      {% for form in formset %}\n        {% include \'yourapp/form.html\' with form=form %}\n      {% endfor %}\n    </div>\n\n    <button class="formset"\n            data-empty-form="{{ empty_form }}"\n            data-prefix="{{ formset.prefix }}">\n      Add form\n    </button>\n  </div>\n\n  <script src="{% static \'coral_formsets/js/FormSet.js\' %}"></script>\n  <script>\n    document.querySelectorAll(\'.formset\').forEach(el => {\n      new window.coral.FormSet(el);\n    });\n  </script>\n</body>\n</html>\n```\n\nA templatetag `render_empty_form_template` irá transformar o seu `formset.empty_form` em texto, para depois fazer a inserção do novo form via javascript.\n',
    'author': 'Cleiton Lima',
    'author_email': 'cleiton.limapin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/coral-sistemas/coral-formsets',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
