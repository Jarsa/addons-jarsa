# -*- coding: utf-8 -*-
# Copyright 2017, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, models
from openerp.exceptions import Warning as validationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def print_report(self):
        for line in self.pack_operation_ids:
            stock_move = self.env['stock.move'].search(
                [('restrict_lot_id', '=', line.lot_id.id),
                 ('production_id', '!=', False)], limit=1)
            production_order = stock_move.production_id
            if not production_order.cloth_type:
                raise validationError(_('The products has not a cloth type'))
        context = dict(
            self.env.context or {},
            active_ids=[self.id],
            active_model='stock.picking')
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'mrp_workflow_print_label.shipment',
            'context': context,
            'docs': self.id}

    @api.model
    def _get_type(self):
        for rec in self:
            list_type = []
            for line in rec.pack_operation_ids:
                stock_move = self.env['stock.move'].search(
                    [('restrict_lot_id', '=', line.lot_id.id),
                     ('production_id', '!=', False)], limit=1)
                production_order = stock_move.production_id
                list_type.append(production_order.cloth_type)
            str_list_type = list(set(list_type))
            return str_list_type[0]

    @api.model
    def _get_data(self):
        for rec in self:
            lines = [[], []]
            for line in rec.pack_operation_ids:
                lots = []
                stock_move = self.env['stock.move'].search(
                    [('restrict_lot_id', '=', line.lot_id.id),
                     ('production_id', '!=', False)], limit=1)
                production_order = stock_move.production_id
                for mrp_line in production_order.move_lines2:
                    lots.append(mrp_line.restrict_lot_id.name)
                if production_order.cloth_type == 'cloth':
                    lines[0].append({
                        'code': line.product_id.default_code,
                        'product': line.product_id.name,
                        'cloth_rolls': ','.join(list(set(filter(
                            lambda a: a is not False, lots)))),
                        'cut_lot': line.lot_id.name,
                        'quantity': line.product_qty,
                    })
                elif production_order.cloth_type == 'cover':
                    lines[1].append({
                        'code': line.product_id.default_code,
                        'product': line.product_id.name,
                        'cut_rolls': ','.join(list(set(filter(
                            lambda a: a is not False, lots)))),
                        'print_lot': line.lot_id.name,
                        'quantity': line.product_qty,
                    })
        return lines
