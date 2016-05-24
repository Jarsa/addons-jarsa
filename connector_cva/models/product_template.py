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
        user_id = self.env.user.company_id.cva_user
        for product in product_list:
            params = {
                'cliente': user_id,
                'clave': product.default_code,
                'MonedaPesos': '1',
                'sucursales': '1',
            }
            root = cva.connect_cva(params=params)
            if len(root) == 0:
                pass
            elif len(root) >= 1:
                for item in root:
                    if item.findtext('clave') == product.default_code:
                        cva.update_product_qty(product.id, item)
                        product.standard_price = float(
                            item.findtext('precio'))
