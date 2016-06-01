# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AcquirerConekta(models.Model):
    _inherit = 'payment.acquirer'

    conekta_public_key = fields.Char(required_if_provider='conekta')
    conekta_private_key = fields.Char(required_if_provider='conekta')

    @api.model
    def _get_providers(self):
        providers = super(AcquirerConekta, self)._get_providers()
        providers.append(['conekta', 'Conekta'])
        return providers

    @api.multi
    def conekta_get_form_action_url(self):
        self.ensure_one()
        return '/shop/payment/validate'
