# -*- coding: utf-8 -*-
# © <2016> <DRC Systems - ported by Jarsa Sistemas S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class StockConfigSettings(models.Model):
    _inherit = 'stock.config.settings'

    group_website_minimum_stock = fields.Integer(
        string='Product Minimum Stock Display message on website',
        help="Give the Minimum value of stock when left stock \
            message display on website.",
        default=5)
