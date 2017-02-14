# -*- coding: utf-8 -*-
# Copyright 2017 <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models


class HelpDeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    task_ids = fields.Many2many(
        comodel_name='project.task',
        string='Tasks')
    nbr_tasks = fields.Integer(
        string='Tasks',
        compute='_compute_nbr_tasks',)

    @api.depends('task_ids')
    def _compute_nbr_tasks(self):
        for rec in self:
            rec.nbr_tasks = len(rec.task_ids)

    @api.multi
    def show_task(self):
        return {
            'name': _('Project Task'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'project.task',
            'domain': [(
                'id', 'in', [x.id for x in self.task_ids])],
            'type': 'ir.actions.act_window',
        }
