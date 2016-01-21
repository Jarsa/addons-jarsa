# -*- coding: utf-8 -*-
from openerp.osv import orm, fields


class StockConfigSettings(orm.Model):
    _inherit = 'stock.config.settings'

    _columns = {
        'group_website_minimum_stock': fields.integer('Product Minimum Stock Display message on website', help="Give the Minimum value of stock when left stock message display on website.")
    }

    _defaults = {
        'group_website_minimum_stock': 5,
    }
