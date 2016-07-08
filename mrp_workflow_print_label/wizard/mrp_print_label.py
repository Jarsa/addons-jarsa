# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class MrpPrintLabel(models.TransientModel):
    _name = 'mrp.print.label'

    print_lot = fields.Char(string="Printing Lot")
    container_qty = fields.Integer(string='Quantity per Container')
    order_id = fields.Many2one(
        'mrp.production', string="Order", readonly=True)

    @api.multi
    def print_report(self):
        self.order_id.write({
            'container_qty': self.container_qty,
            'print_lot': self.print_lot,
            })
        self.order_id.message_post(
            body=_("Printed by: %s") % (self.order_id.user_id.name))
        context = dict(
            self.env.context or {},
            active_ids=[self.order_id.id],
            active_model='mrp.production')

        self.order_id.action_production_end()
        if self.order_id.bom_id.cloth:
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'mrp_workflow_print_label.label_cloth',
                'context': context,
                'docs': self.order_id.id
            }
        else:
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'mrp_workflow_print_label.label_cut',
                'context': context,
                'docs': self.order_id.id
            }
