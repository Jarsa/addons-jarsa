# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    state = fields.Selection([
        ('draft', 'New'),
        ('cancel', 'Cancelled'),
        ('confirmed', 'Awaiting Raw Materials'),
        ('ready', 'Ready to Produce'),
        ('in_production', 'Production Started'),
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
    cloth_type = fields.Selection(related='bom_id.cloth_type')
