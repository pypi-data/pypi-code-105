# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class VhInvoicingOrderItem(models.Model):
  _name = 'vh.invoicing.order.item'
  name= fields.Char(_("Name"))
  partner_id = fields.Many2one('res.partner',string=_("Partner"))
  order_id = fields.Many2one('vh.invoicing.order',string=("Order"))
  invoice_ids = fields.One2many('account.invoice','order_item_id',string=_("Invoices"))