# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    state = fields.Selection([
        ('draft', 'New'),
        ('cancel', 'Cancelled'),
        ('confirmed', 'Awaiting Raw Materials'),
        ('ready', 'Ready to Produce'),
        ('in_production', 'Production Started'),
        ('print_label', _('Print Label')),
        ('done', 'Done')])
    print_lot = fields.Char(string="Printing Lot", readonly=True)
    container_qty = fields.Integer(string='Quantity per Lot', readonly=True)
    components_number = fields.Integer(
        string="Components Number", readonly=True)
    components_pieces = fields.Integer(
        string="Components Pieces", readonly=True)
    cloth_rolls = fields.Char(string="Cloth Rolls", readonly=True)
    total_pieces = fields.Integer(readonly=True)
    print_lot_barcode = fields.Binary(readonly=True)
    production_barcode = fields.Binary(readonly=True)
    cloth_type = fields.Selection(related='bom_id.cloth_type')
    produce_button = fields.Boolean(
        string='Button Produce',
        compute="_compute_produce_button",
        store=True,
    )
    print_button = fields.Boolean(
        string='Print Button',
        compute="_compute_print_button",
        store=True,
    )

    @api.multi
    def action_state_print_label(self):
        for rec in self:
            if self.bom_id.cloth_type in ['cover', 'cloth']:
                rec.state = 'print_label'
            else:
                self.action_production_end()

    @api.depends('move_lines', 'state')
    def _compute_produce_button(self):
        for rec in self:
            if (not rec.move_lines or
                    rec.state not in
                    ['print_label', 'ready', 'in_production']):
                rec.produce_button = True
            else:
                rec.produce_button = False

    @api.depends('move_lines2', 'state', 'cloth_type')
    def _compute_print_button(self):
        for rec in self:
            if (not rec.cloth_type or
                    rec.state not in ['print_label', 'in_production'] or
                    not rec.move_lines2):
                rec.print_button = False
            else:
                rec.print_button = True
