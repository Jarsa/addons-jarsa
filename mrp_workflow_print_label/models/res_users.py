# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'
    _name = 'res.users'

    mrp_pin = fields.Char(
        string='PIN',
    )

    _sql_constraints = [(
        'mrp_pin_unique', 'UNIQUE(mrp_pin)', _("The PIN must be unique")),
    ]
