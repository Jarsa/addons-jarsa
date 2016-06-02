# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import logging
import requests
import datetime

from openerp import api, fields, models
from openerp.tools.translate import _
from openerp.addons.payment.models.payment_acquirer import ValidationError

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    conekta_oxxo_barcode = fields.Binary(string='Oxxo Barcode')
    conekta_oxxo_expire_date = fields.Date(string="Oxxo expire date")

    @api.model
    def _conekta_oxxo_form_get_tx_from_data(self, data):
        reference = data['reference_id']
        payment_tx = self.search([('reference', '=', reference)])
        if not payment_tx or len(payment_tx) > 1:
            error_msg = _(
                'Conekta: received data for reference %s') % reference
            if not payment_tx:
                error_msg += _('; no order found')
            else:
                error_msg += _('; multiple order found')
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        return payment_tx

    @api.model
    def _conekta_oxxo_form_validate(self, transaction, data):
        date = datetime.datetime.fromtimestamp(
            int(data.payment_method['expires_at'])).strftime(
                '%Y-%m-%d %H:%M:%S')
        data = {
            'acquirer_reference': data['id'],
            'state': 'pending',
            'conekta_oxxo_barcode': base64.encodestring(
                requests.get(data.payment_method['barcode_url']).content),
            'conekta_oxxo_expire_date': date,
        }
        transaction.write(data)
