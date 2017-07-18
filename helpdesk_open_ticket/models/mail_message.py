# -*- coding: utf-8 -*-
# Copyright 2017, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def create(self, vals):
        active_model = vals.get('model', False)
        if active_model == 'helpdesk.ticket':
            ticket = self.env[active_model].browse(vals['res_id'])
            if (ticket.stage_id.is_close and
                    vals['author_id'] !=
                    self.env.user.partner_id.id):
                stage = self.env['helpdesk.stage'].search(
                    [('team_ids', 'in', ticket.team_id.id)],
                    order='sequence', limit=1)
                ticket.stage_id = stage.id or False
                ticket.user_id = False
        return super(MailMessage, self).create(vals)
