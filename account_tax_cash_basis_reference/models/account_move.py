# -*- coding: utf-8 -*-
# Copyright 2017, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    nbr_moves = fields.Float(
        string=_('Tax Moves'), compute="_compute_nbr_moves",
        default=0,)
    account_move_ids = fields.One2many(
        'account.move',
        'move_id',
        string='Account Move',
    )
    move_id = fields.Many2one(
        'account.move',
    )

    @api.multi
    def _compute_nbr_moves(self):
        for rec in self:
            if rec.account_move_ids:
                rec.nbr_moves = len(rec.account_move_ids)

    @api.multi
    def account_move(self):
        return {
            'name': _('Account Move'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [(
                'move_id', '=', self.id)],
            'type': 'ir.actions.act_window',
            'context': {
                'create': False,
                'delete': False
            }
        }
