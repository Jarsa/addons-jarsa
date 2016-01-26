# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, http
from openerp.addons.website_sale.controllers.main import website_sale


class WebsiteSale(website_sale):

    @http.route(['/shop/product/<model("product.template"):product>'],
                type='http', auth="public", website=True)
    @api.multi
    def product(self, args):
        resp = super(WebsiteSale, self).product(self, args)

        settings_obj = self.env['stock.config.settings'].search(limit=1,
                                                                order='id DES')
        if settings_obj:
            resp.qcontext['min_stock'] = (settings_obj.
                                          group_website_minimum_stock)
        return resp
