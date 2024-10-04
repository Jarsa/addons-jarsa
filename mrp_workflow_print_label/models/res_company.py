from openerp import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    supplier_number = fields.Char()
