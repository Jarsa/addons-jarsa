# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class MrpPrintLabelValidate(models.TransientModel):
    _name = 'mrp.print.label.validate'

    pin = fields.Char(string='PIN')
    order_id = fields.Many2one('mrp.production')
    container_qty = fields.Integer(string='Quantity per Lot')
    bom_cloth = fields.Selection(related='order_id.bom_id.cloth_type')
    reason_id = fields.Many2one(
        'mrp.print.reason', string='Reason for Re-Printing', required=True)

    @api.model
    def default_get(self, field):
        production_obj = self.env['mrp.production']
        record_id = self.env.context['active_id']
        production = production_obj.search([('id', '=', record_id)])
        res = super(MrpPrintLabelValidate, self).default_get(field)
        res.update({'container_qty': production.container_qty})
        return res

    @api.multi
    def validate(self):
        user = self.env['res.users'].search(
            [('mrp_pin', '=', self.pin)])
        if len(user) == 0 or self.pin is False:
            raise UserError(_('Invalid PIN'))
        else:
            self.order_id.write({'container_qty': self.container_qty})
            message = _(
                "Re-Print Authorized by: %s <br/> Re-Printed Reason: %s") % (
                user.name, self.reason_id.name)
            if self.bom_cloth == 'cover':
                message = message + _(
                    '<br/> Container Quantity: %s' % self.container_qty)
            self.order_id.message_post(body=message)
            context = dict(
                self.env.context or {},
                active_ids=[self.order_id.id],
                active_model='mrp.production')
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
