# -*- coding: utf-8 -*-
{
  'name': "vertical-habitatge",

  'summary': """
    Base for habitatge.""",

  'author': "Coopdevs",
  'website': "https://gitlab.com/coopdevs/vertical-habitatge",

  # Categories can be used to filter modules in modules listing
  # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
  # for the full list
  'category': 'vertical-habitatge',
  'version': '12.0.0.0.2',

  # any module necessary for this one to work correctly
  'depends': ['base'],

  # always loaded
  'data': [
    'views/vh_menu_root.xml',
    'views/vh_menu_root_config.xml',
    'views/vh_partner.xml'
  ],
}
