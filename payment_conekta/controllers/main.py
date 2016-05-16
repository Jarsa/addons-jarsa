# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from openerp import http, _
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
        so_id = http.request.session['sale_order_id']
        so = http.request.env['sale.order'].search([('id', '=', so_id)])
        params = {}
        params['description'] = so.name
        params['amount'] = int(so.amount_total * 100)
        params['currency'] = so.currency_id.name
        params['reference_id'] = so.name
        params['card'] = token_id
        details = params['details'] = {}
        details['name'] = so.partner_id.name
        details['phone'] = so.partner_id.phone
        details['email'] = so.partner_id.email
        customer = details['customer'] = {}
        if http.request.session['uid'] is not None:
            # TODO: "offline_payments" and "score"
            customer['logged_in'] = True
            customer['successful_purchases'] = so.partner_id.sale_order_count
            customer['created_at'] = so.partner_id.create_date
            customer['updated_at'] = so.partner_id.write_date
        else:
            customer['logged_in'] = False
        line_items = details['line_items'] = []
        for order_line in so.order_line:
            item = {}
            line_items.append(item)
            item['name'] = order_line.product_id.name
            item['description'] = _('%s Order %s' % (so.company_id.name,
                                                     so.name))
            item['unit_price'] = order_line.price_unit
            item['quantity'] = order_line.product_uom_qty
            item['sku'] = order_line.product_id.default_code
            item['category'] = order_line.product_id.categ_id.name
        billing_address = details['billing_address'] = {}
        billing_address['street1'] = so.partner_invoice_id.street
        billing_address['street2'] = so.partner_invoice_id.street2
        billing_address['city'] = so.partner_invoice_id.city
        billing_address['state'] = so.partner_invoice_id.state_id.code
        billing_address['zip'] = so.partner_invoice_id.zip
        billing_address['country'] = so.partner_invoice_id.country_id.name
        billing_address['tax_id'] = so.partner_invoice_id.vat
        billing_address['company_name'] = (so.partner_invoice_id.parent_name or
                                           so.partner_invoice_id.name)
        billing_address['phone'] = so.partner_invoice_id.phone
        billing_address['email'] = so.partner_invoice_id.email
        test = conekta.Charge.create(params)
        print test.status
        return str(test.status)
