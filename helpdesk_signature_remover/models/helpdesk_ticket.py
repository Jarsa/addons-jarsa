# -*- coding: utf-8 -*-
# Copyright 2017, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.tools import html2plaintext


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    @api.multi
    def clean_signatures(self):
        for rec in self:
            for signature in self.env['signature.remover'].search([]):
                sig = html2plaintext(
                    signature.signature).replace('\n', '')
                for msg in rec.message_ids:
                    body = html2plaintext(msg.body).replace('\n', '')
                    if body.find(sig) != -1:
                        msg.write({
                            'body': body.replace(sig, '')
                        })
