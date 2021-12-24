# -*- coding: utf-8 -*-
from lcyframe.libs import Copyright

class Config(object):
    config_dict = dict(
        extensions = [
            'sphinx.ext.autodoc',
            'sphinx.ext.doctest',
            'sphinx.ext.intersphinx',
            'sphinx.ext.todo',
            'sphinx.ext.coverage',
            'm2r'
        ],
        templates_path = ['_templates'],
        source_suffix = ['.rst', '.md'],
        master_doc = 'index',
        exclude_patterns = [],
        pygments_style = 'sphinx',
        todo_include_todos = True,
        latex_elements = {},
        html_sidebars = {
            '**': [
                'about.html',
                'navigation.html',
                'relations.html',
                'searchbox.html',
                'donate.html',
            ]
        },
        project = u'LcyFrame',
        copyright = u'2017, Lcylln',
        author = u'Lcylln',
        version = u'',
        release = u'',
        language = 'zh_CN',
        html_theme = 'sphinx_rtd_theme',
        html_static_path = ['template/_static'],
        index_doc_config = {
            'title': "LcyFrame",
            'content': "LcyFrame",
            "nav": []
        },
        errors_doc_config = {
            "if_set_errors": False,
            "module_dir": "/path",
            "module_name": "errors",
            "error_title": "",
        },
        log_doc_config = {
            "if_set_log": False,
            "author": "Lcylln",
            "log_title": "",
        }
    )

    def __init__(self, **kwargs):
        self.path = kwargs.get('path')

    def mk_conf(self, api_schema_dir, errors_dir, constant_dir, table_schema_dir):
        """

        :return:
        """
        conf_str = ""
        conf_str += """# -*- coding: utf-8 -*-
# docs config
#
import sphinx_rtd_theme

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'm2r'
]
templates_path = ['_templates']
source_suffix = ['.rst', '.md']
master_doc = 'index'
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = True
latex_elements = {}
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
        'donate.html',
    ]
}

# set document title author
"""
        conf_str += "\n"
        conf_str += "project = u'" + self.config_dict['project'] + "'"
        conf_str += "\n"
        conf_str += "copyright = u'" + self.config_dict['copyright'] + "'"
        conf_str += "\n"
        conf_str += "author = u'" + self.config_dict['author'] + "'"
        conf_str += "\n"
        conf_str += """
# API version
version = u''
release = u''

# language
language = 'zh_CN'

# theme
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme . get_html_theme_path()]

# static path
html_static_path = ['template/_static']

# index
index_doc_config = {
    'title': "欢迎使用!",
    'content': "Skype：lcylln001@gmail.com",
    "nav": ["agree", "api", "error", "constant", "tables"]
}

# api config
api_doc_config = {
    "if_set_api": True,            # Using YML to generate .md
    "api_schema_dir": "%s",               # abs path of your api_schema dir. like this:xxx/xxx/api_schema/
    "leve": 2,                     #
    "title": "二、接口说明",         # give the title by level start path.
    "schema_template": "lcyframe"  # with yml template。 lcyframe, default
}

# error code config
errors_doc_config = {
    "if_set_errors": True,
    "module_dir": "%s",            # errors.py path, default like '~/www/demo/utils'
    "module_name": "errors",
    "error_title": "三、错误码",
}

# constant config
constant_doc_config = {
    "if_set": True,
    "module_dir": "%s",           # constant.py path, default like '~/www/demo/utils'
    "module_name": "constant",
    "title": "四、常量值",
}

# db table 
table_doc_config = {
    "if_set": True,
    "module_dir": "%s",           # xxx_schema.py path, default like '~/model/schema'
    "module_name": "schema",
    "title": "五、数据库设计",
}

# doc log
log_doc_config = {
    "if_set_log": False,
    "author": "%s",
    "log_title": "五、更新日志",
} 
        """ % (api_schema_dir, errors_dir, constant_dir, table_schema_dir, Copyright.auto_name)

        f = open(self.path + "/conf.py", "w+", encoding='utf-8')
        f.write(conf_str)
        f.close()

