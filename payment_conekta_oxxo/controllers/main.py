# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from openerp import http
from openerp.http import request
from openerp.addons.payment_conekta.controllers.main import ConektaController

_logger = logging.getLogger(__name__)
try:
    import conekta
except:
    _logger.debug('Cannot `import conekta`.')


class ConektaOxxoController(ConektaController):

    def conekta_oxxo_validate_data(self, data):
        res = False
        tx_obj = request.env['payment.transaction']
        res = tx_obj.sudo().form_feedback(data, 'conekta_oxxo')
        return res

    @http.route('/payment/conekta/oxxo/charge', type='json',
                auth='public', website=True)
    def charge_oxxo_create(self, **kwargs):
        payment_acquirer = request.env['payment.acquirer']
        conekta_acq = payment_acquirer.sudo().search(
            [('provider', '=', 'conekta')])
        conekta.api_key = conekta_acq.conekta_private_key
        params = self.create_params('conekta_oxxo')
        try:
            response = conekta.Charge.create(params)
        except conekta.ConektaError as error:
            return error.message['message_to_purchaser']
        self.conekta_oxxo_validate_data(response)
        return True
