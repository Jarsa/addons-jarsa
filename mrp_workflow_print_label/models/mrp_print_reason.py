# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class MrpPrintReason(models.Model):
    _name = 'mrp.print.reason'
    _description = 'Reason for reprinting label'

    name = fields.Char(required=True)
