from openerp import api, http
from openerp.addons.website_sale.controllers.main import website_sale


class WebsiteSale(website_sale):

    @http.route(['/shop/product/<model("product.template"):product>'],
                type='http', auth="public", website=True)
    @api.multi
    def product(self):
        resp = super(WebsiteSale, self).product(self)

        settings_obj = self.env['stock.config.settings']
        config_ids = settings_obj.search(limit=1, order='id DESC')
        if config_ids:
            resp.qcontext['min_stock'] = (config_ids.
                                          group_website_minimum_stock)
        return resp
