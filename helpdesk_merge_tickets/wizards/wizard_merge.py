# -*- coding: utf-8 -*-
# © <2017> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class WizardMerge(models.TransientModel):
    _name = 'wizard.merge'
    _description = 'Merge Incidents'

    incident_ids = fields.Many2many(
        'helpdesk.ticket',
        string='Incidents',
    )
    incident = fields.Selection(
        selection='get_incident',
        string="Main Incident",)

    @api.model
    def get_incident(self):
        selection_incident = []
        if 'active_ids' in self._context:
            active_model = self.env.context['active_model']
            for line in self.env[active_model].search(
                    [('id', 'in', self._context['active_ids'])]):
                selection_incident.append((line.id, line.name.encode('utf-8')))
        return selection_incident

    @api.model
    def default_get(self, values):
        res = super(WizardMerge, self).default_get(values)
        active_ids = self.env.context['active_ids'] or []
        res['incident_ids'] = active_ids
        return res

    @api.multi
    def merge(self):
        for rec in self:
            main = self.env['helpdesk.ticket'].search(
                [('id', '=', int(rec.incident.encode('utf-8')))])
            for line in rec.incident_ids:
                attachments = self.env['ir.attachment'].search([
                    ('res_model', '=', 'helpdesk.ticket'),
                    ('res_id', '=', line.id)])
                followers = self.env['mail.followers'].search([
                    ('res_model', '=', 'helpdesk.ticket'),
                    ('res_id', '=', line.id)])

                for follower in followers:
                    if (follower.partner_id not in
                            main.message_follower_ids.mapped('partner_id')):
                        follower.write({'res_id': main.id})
                for attachment in attachments:
                    attachment.write({
                        'res_id': main.id,
                        'res_name': main.name,
                    })
                for msg in line.message_ids:
                    msg.write({
                        'res_id': main.id,
                        'record_name': main.name,
                    })
                if line.id != main.id:
                    line.unlink()
