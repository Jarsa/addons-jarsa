# -*- coding: utf-8 -*-
# © <2015> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    @api.multi
    def update_price(self):
        cva = self.env['cva.config.settings']
        client = self.env.user.company_id.cva_user
        params = {
            'cliente': client,
            'descripcion': self.name,
            'clave': self.default_code,
        }
        print params
        root = cva.connect_cva(params=params)
        for item in root:
            if item.findtext('clave') == self.default_code:
                self.write({
                    'standard_price':
                        float(item.findtext('precio'))
                })
                return self.standard_price
