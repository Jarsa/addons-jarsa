# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class AcquirerConektaOxxo(models.Model):
    _inherit = 'payment.acquirer'

    @api.model
    def _get_providers(self):
        providers = super(AcquirerConektaOxxo, self)._get_providers()
        providers.append(['conekta_oxxo', 'Oxxo'])
        return providers

    @api.multi
    def conekta_oxxo_get_form_action_url(self):
        self.ensure_one()
        return '/shop/payment/validate'
