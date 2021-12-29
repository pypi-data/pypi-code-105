from odoo import models, fields, api
from odoo.tools.translate import _

class VhPartner(models.Model):
  _inherit = 'res.partner'

  # App Person Contact fields
  type = fields.Selection(selection_add=[
    ('house_contact', _("House")),
    ('inhabitant_contact', _("Inhabitant")),
  ])