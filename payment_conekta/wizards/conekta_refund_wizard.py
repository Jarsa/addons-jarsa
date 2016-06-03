# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models

from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

try:
    import conekta
except:
    _logger.debug('Cannot `import conekta`.')


class ConektaRefundWizard(models.TransientModel):
    _name = 'conekta.refund.wizard'

    message = fields.Text(placeholder="Motive of refund", required=True)
    sale_order_id = fields.Many2one('sale.order', readonly=True)
    amount = fields.Float(string='Amount to refund', required=True)

    @api.multi
    def conekta_refund_card(self):
        acquirer = self.env.ref('payment_conekta.payment_acquirer_conekta')
        tx = self.sale_order_id.payment_tx_id
        conekta.api_key = acquirer.conekta_private_key
        charge = conekta.Charge.find(tx.acquirer_reference)
        charge.refund(amount=int(self.amount*100))
        if charge.status in ['refunded', 'partially_refunded']:
            if charge.status == 'refunded':
                tx.state = 'cancel'
                status = _('Refunded')
            if charge.status == 'partially_refunded':
                status = _('Partially Refunded')
            message = _('<b>Payment refund complete.</b></br><ul>'
                        '<li><b>Transaction Status: </b>%s</li>'
                        '<li><b>Amount refunded: </b>%s %s</li>'
                        '<li><b>Message: </b>%s</li>'
                        '</ul><br/>') % (status, self.amount,
                                         self.sale_order_id.currency_id.name,
                                         self.message)
            self.sale_order_id.message_post(body=message)
