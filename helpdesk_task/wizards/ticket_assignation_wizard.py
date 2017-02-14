# -*- coding: utf-8 -*-
# Copyright 2017, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models

TICKET_PRIORITY = [
    ('0', 'All'),
    ('1', 'Low priority'),
    ('2', 'High priority'),
    ('3', 'Urgent'),
]


class TicketAssignationWizard(models.TransientModel):
    _name = 'ticket.assignation.wizard'

    ticket_id = fields.Many2one(
        comodel_name='helpdesk.ticket',
        string='HelpDesk Ticket',
        readonly=True, )
    action_type = fields.Selection(
        [('create', 'Create New Task'),
         ('add', 'Add to Task created.')],
        string='Action',
        default='create',)
    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project')
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsible',)
    task_id = fields.Many2one(
        comodel_name='project.task',
        string='Task',)
    priority = fields.Selection(
        TICKET_PRIORITY,
        string='Priority',
        default='0',)
    task_ids = fields.Many2many(
        comodel_name='project.task',
        string='Tasks',)

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id:
            return {'domain': {'task_id': [
                ('project_id', '=', self.project_id.id),
                ('id', 'not in', [x.id for x in self.task_ids])]}}

    @api.onchange('task_id')
    def _onchange_task_id(self):
        if self.task_id:
            self.project_id = self.task_id.project_id.id

    @api.model
    def default_get(self, fields):
        res = super(TicketAssignationWizard, self).default_get(
            fields)
        helpdesk_obj = self.env['helpdesk.ticket']
        active_ids = self.env.context['active_ids'] or []
        active_model = self.env.context['active_model']

        if not active_ids:
            return res
        assert active_model == 'helpdesk.ticket', \
            'Bad context propagation'
        for line in helpdesk_obj.browse(active_ids):
            res['ticket_id'] = line.id
            res['user_id'] = line.user_id.id
            res['priority'] = line.priority
            res['task_ids'] = [(6, 0, [x.id for x in line.task_ids])]
        return res

    @api.multi
    def ticket_assign(self):
        for rec in self:
            if rec.action_type == 'create':
                task = self.env['project.task'].create({
                    'name': rec.ticket_id.name,
                    'project_id': rec.project_id.id,
                    'user_id': rec.user_id.id,
                    'ticket_ids': [(4, rec.ticket_id.id)],
                    'priority': rec.priority,
                    })
            else:
                rec.task_id.write({
                    'project_id': rec.project_id.id,
                    'user_id': rec.user_id.id,
                    'ticket_ids': [(4, rec.ticket_id.id)],
                    'priority': rec.priority,
                    })
                task = rec.task_id
            rec.ticket_id.write({
                'task_ids': [(4, task.id)],
                })
        return {
            'name': _('Project Task'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'project.task',
            'res_id': task.id,
            'target': 'current',
            'type': 'ir.actions.act_window',
        }
