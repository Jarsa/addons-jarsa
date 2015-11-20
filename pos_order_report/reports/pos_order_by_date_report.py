from openerp import api, models


class PosOrderByDateReport(models.AbstractModel):
    _name = 'report.pos_order_report.report_pos_order_by_date'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('pos_order_report.report_pos_order_by_date')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'data': data,
            'get_warehouse': self._get_warehouse,
        }
        return report_obj.render('pos_order_report.report_pos_order_by_date', docargs)
    
    def _get_warehouse(self, warehouse_id):
        warehouse_obj = self.env['stock.warehouse']
        warehouse = warehouse_obj.browse([warehouse_id[0]])
        return warehouse.name