# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    payment_tx_status = fields.Boolean(compute='_compute_payment_tx_status')

    @api.depends('payment_tx_id')
    def _compute_payment_tx_status(self):
        for rec in self:
            if rec.payment_tx_id:
                if rec.payment_tx_id.state == 'done' and (
                   rec.payment_tx_id.acquirer_id.provider == 'conekta'):
                    rec.payment_tx_status = True
                else:
                    rec.payment_tx_status = False
            else:
                rec.payment_tx_status = False
