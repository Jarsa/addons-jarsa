# -*- coding: utf-8 -*-
# Copyright 2017, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    lot_ids = fields.Char(
        string='Lots',
    )
