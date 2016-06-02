# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from openerp import http, _
from openerp.http import request
from datetime import datetime
from time import mktime
_logger = logging.getLogger(__name__)
try:
    import conekta
except:
    _logger.debug('Cannot `import conekta`.')


class ConektaController(http.Controller):

    def conekta_validate_data(self, data):
        res = False
        tx_obj = request.env['payment.transaction']
        res = tx_obj.sudo().form_feedback(data, 'conekta')
        return res

    def create_params(self, acquirer):
        so_id = request.session['sale_order_id']
        so = request.env['sale.order'].sudo().search([('id', '=', so_id)])
        params = {}
        params['description'] = _('%s Order %s' % (so.company_id.name,
                                                   so.name))
        params['amount'] = int(so.amount_total * 100)
        params['currency'] = so.currency_id.name
        params['reference_id'] = so.name
        if acquirer == 'conekta':
            params['card'] = request.session['conekta_token']
        if acquirer == 'conekta_oxxo':
            params['cash'] = {'type': 'oxxo'}
            # TODO: ADD expires_at
        details = params['details'] = {}
        details['name'] = so.partner_id.name
        details['phone'] = so.partner_id.phone
        details['email'] = so.partner_id.email
        customer = details['customer'] = {}
        if request.session['uid'] is not None:
            # TODO: "offline_payments" and "score"
            create_at = so.partner_id.create_date
            create_date = mktime(datetime.strptime(
                create_at, '%Y-%m-%d %H:%M:%S').timetuple())
            write_at = so.partner_id.write_date
            updated_date = mktime(datetime.strptime(
                write_at, '%Y-%m-%d %H:%M:%S').timetuple())
            customer['logged_in'] = True
            customer['successful_purchases'] = so.partner_id.sale_order_count
            customer['created_at'] = str(create_date)
            customer['updated_at'] = str(updated_date)
        else:
            customer['logged_in'] = False
        line_items = details['line_items'] = []
        for order_line in so.order_line:
            item = {}
            line_items.append(item)
            item['name'] = order_line.product_id.name
            item['description'] = order_line.product_id.description_sale
            item['unit_price'] = int(order_line.price_unit * 100)
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
        return params

    @http.route('/payment/conekta/charge', type='json',
                auth='public', website=True)
    def charge_create(self, token):
        request.session['conekta_token'] = token
        payment_acquirer = request.env['payment.acquirer']
        conekta_acq = payment_acquirer.sudo().search(
            [('provider', '=', 'conekta')])
        conekta.api_key = conekta_acq.conekta_private_key
        params = self.create_params('conekta')
        try:
            response = conekta.Charge.create(params)
        except conekta.ConektaError as error:
            return error.message['message_to_purchaser']
        self.conekta_validate_data(response)
        return True
