# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from openerp import api, models

from datetime import datetime

_logger = logging.getLogger(__name__)


class Webhook(models.Model):
    _inherit = 'webhook'

    @api.multi
    def run_conekta_charge_paid(self):
        tx_obj = self.env['payment.transaction']
        request = self.env.request.jsonrequest
        tx_ref = request['data']['object']['reference_id']
        tx = tx_obj.search([('reference', '=', tx_ref)])
        date = datetime.fromtimestamp(
            int(request['data']['object']['paid_at'])).strftime(
                '%Y-%m-%d %H:%M:%S')
        if request['data']['object']['status'] == 'paid':
            tx.state = 'done'
            tx.date_validate = date
