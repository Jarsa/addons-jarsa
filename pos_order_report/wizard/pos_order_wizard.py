# -*- coding: utf-8 -*-
from openerp import models, fields, api


class wizard(models.TransientModel):
    _name = 'pos.order.wizard'

    date_start = fields.Date(required=True, default=fields.Date.today)
    date_end = fields.Date(required=True, default=fields.Date.today)
    warehouse_id = fields.Many2one('stock.warehouse',
        string="Warehouse", required=True)

    def print_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.read(cr, uid, ids)[0]
        datas = {
            'ids': context.get('active_ids', []),
            'model': 'pos.order',
            'form': data
        }

        datas['form']['active_ids'] = context.get('active_ids', False)

        return self.pool['report'].get_action(cr, uid, [], 'pos_order_report.pos_order_by_date_report', data=datas, context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

