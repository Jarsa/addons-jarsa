# -*- coding: utf-8 -*-
# © <2015> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class StockChangeProductQty(models.Model):
    _name = 'stock.change.product.qty'
    _inherit = 'stock.change.product.qty'

    @api.onchange('location_id')
    def onchange_location_id(self):
        if self.location_id:
            qty = self.env['product.template']._product_available(
                [self.product_id],
                context=dict(location=self.location_id))
            if self.product_id in qty:
                location = self.env['stock.location']
                cva = self.env['cva.config.settings']
                client = self.env.user.company_id.cva_user
                location_list = [x.name for x in location.search([])]
                for item in location_list:
                    params = {
                        'cliente': client,
                        'sucursales': '1',
                    }
                    root = cva.connect_cva(params)
                    for prd in root:
                        self.new_quantity = prd.findtext(prd)
                    return self.new_quantity
