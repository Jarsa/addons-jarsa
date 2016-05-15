# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from openerp import http
from openerp.addons.website_sale.controllers.main import website_sale

_logger = logging.getLogger(__name__)
try:
    import conekta
except:
    _logger.debug('Cannot `import conekta`.')


class ConektaController(website_sale):

    @http.route()
    def payment(self):
        payment = super(ConektaController, self).payment()
        payment_acquirer = http.request.env['payment.acquirer']
        conekta_acq = payment_acquirer.search([('provider', '=', 'conekta')])
        values = payment.qcontext
        values['conekta'] = conekta_acq
        return http.request.render('website_sale.payment', values)

    @http.route('/conekta/charge', auth='public', website=True)
    def charge_create(self, **kw):
        payment_acquirer = http.request.env['payment.acquirer']
        conekta_acq = payment_acquirer.search([('provider', '=', 'conekta')])
        conekta.api_key = conekta_acq.conekta_private_key
        token_id = http.request.params.copy()['token_id']
        params = {
            "description": "Stogies",
            "amount": 20000,
            "currency": "MXN",
            "reference_id": "9839-wolf_pack",
            "card": token_id,
            "details": {
                "name": "Arnulfo Quimare",
                "phone": "403-342-0642",
                "email": "logan@x-men.org",
                "customer": {
                    "logged_in": True,
                    "successful_purchases": 14,
                    "created_at": 1379784950,
                    "updated_at": 1379784950,
                    "offline_payments": 4,
                    "score": 9
                    },
                "line_items": [{
                    "name": "Box of Cohiba S1s",
                    "description": "Imported From Mex.",
                    "unit_price": 20000,
                    "quantity": 1,
                    "sku": "cohb_s1",
                    "category": "food"
                }],
                "billing_address": {
                    "street1": "77 Mystery Lane",
                    "street2": "Suite 124",
                    "street3": '',
                    "city": "Darlington",
                    "state": "NJ",
                    "zip": "10192",
                    "country": "Mexico",
                    "tax_id": "xmn671212drx",
                    "company_name": "X-Men Inc.",
                    "phone": "77-777-7777",
                    "email": "purshasing@x-men.org"
                }
                }
            }
        test = conekta.Charge.create(params)
        print test.status
        return str(test.status)
