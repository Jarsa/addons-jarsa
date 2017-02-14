# -*- coding: utf-8 -*-
# Copyright 2017, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models

TICKET_PRIORITY = [
    ('0', 'New'),
    ('1', 'Low priority'),
    ('2', 'High priority'),
    ('3', 'Urgent'),
]


class ProjectTask(models.Model):
    _inherit = 'project.task'

    ticket_ids = fields.Many2many(
        comodel_name='helpdesk.ticket',
        string='Tickets',)
    nbr_tickets = fields.Integer(
        string='Tickets',
        compute='_compute_nbr_tickets',)
    priority = fields.Selection(
        TICKET_PRIORITY,
        string='Priority',
        default='0',
    )

    @api.depends('ticket_ids')
    def _compute_nbr_tickets(self):
        for rec in self:
            rec.nbr_tickets = len(rec.ticket_ids)

    @api.multi
    def show_tickets(self):
        return {
            'name': _('Helpdesk Tickets'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'helpdesk.ticket',
            'domain': [(
                'id', 'in', [x.id for x in self.ticket_ids])],
            'type': 'ir.actions.act_window',
        }
