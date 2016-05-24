# -*- coding: utf-8 -*-
# © <2015> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    @api.multi
    def update_price_multi(self, model=None):
        product_list = self.search(
            [('id', 'in', self.env.context['active_ids'])])
        cva = self.env['cva.config.settings']
        cva.update_product(product_list)
