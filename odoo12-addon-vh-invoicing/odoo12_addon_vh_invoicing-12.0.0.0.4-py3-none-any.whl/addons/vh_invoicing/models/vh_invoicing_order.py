# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class VhInvoicingOrder(models.Model):
  _name = 'vh.invoicing.order'

  name= fields.Char(_("Name"))

  account_journal_mids = fields.Many2many('account.journal', 
    'vh_invoicing_order_account_journal', 'invoicing_order_id',
    'account_journal_id', string=_("Account journals"))

  contact_group_id = fields.Many2one('vh.invoicing.contact.group')

  order_item_ids = fields.One2many('vh.invoicing.order.item','order_id',string="Order Items")