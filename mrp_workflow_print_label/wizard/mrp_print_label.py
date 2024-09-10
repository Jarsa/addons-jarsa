# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
import base64


class MrpPrintLabel(models.TransientModel):
    _name = 'mrp.print.label'

    print_lot = fields.Char(string="Printing Lot")
    container_qty = fields.Integer(string='Quantity per Container')
    order_id = fields.Many2one(
        'mrp.production', string="Order", readonly=True)
    bom_cloth = fields.Selection(related='order_id.bom_id.cloth_type')
    components_number = fields.Integer(string="Components Number")
    components_pieces = fields.Integer(string="Components Pieces")
    total_pieces = fields.Integer(readonly=True)

    @api.multi
    def print_report(self):
        self.order_id.state = "print_label"
        message = _("Printed by: %s") % self.order_id.user_id.name
        if self.order_id.bom_id.cloth_type == 'cloth':
            image = self.env['report'].barcode(
                'QR', self._prepare_qr_code(),
                width=300, height=300)
            image_b64 = base64.encodestring(image)
        else:
            message = message + _(
                '<br/>Container Quantity: %s') % self.container_qty
            image = self.env['report'].barcode(
                'QR', self._prepare_qr_code(),
                width=300, height=300)
            image_b64 = base64.encodestring(image)
        self.order_id.write({
            'components_number': self.components_number,
            'components_pieces': self.components_pieces,
            'total_pieces': self.components_pieces * self.components_number,
            'container_qty': self.container_qty,
            'print_lot': self.print_lot,
            'print_lot_barcode': image_b64,
            })
        self.order_id.message_post(
            body=message)
        context = dict(
            self.env.context or {},
            active_ids=[self.order_id.id],
            active_model='mrp.production')
        if not self.order_id.move_created_ids.product_qty:
            self.order_id.action_production_end()
        if self.order_id.bom_id.cloth_type == 'cloth':
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

    @api.multi
    def _prepare_qr_code(self):
        qr_code = "1J{supplier_number}Q{quantity}P{part_number}V{supplier_number}1T{lot}21L".format(
            supplier_number=self.order_id.company_id.supplier_number,
            quantity=self.total_pieces,
            part_number=self.order_id.product_id.default_code or "",
            lot=self.print_lot)
        return qr_code

    @api.model
    def default_get(self, fields):
        res = super(MrpPrintLabel, self).default_get(fields)
        active_id = self._context['active_id']
        active_model = self._context['active_model']
        order = self.env[active_model].search([('id', '=', active_id)])
        res['components_number'] = order.move_created_ids2[-1].product_qty
        res['components_pieces'] = len(order.bom_id.bom_line_ids)
        res['container_qty'] = order.move_created_ids2[-1].product_qty
        return res
