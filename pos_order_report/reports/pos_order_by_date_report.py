# coding: utf-8` or `# -*- coding: utf-8 -*-
from openerp import api, models
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT as DT
from openerp.tools.misc import DEFAULT_SERVER_DATE_FORMAT as DF
from datetime import datetime, timedelta
import pytz
from pandas import date_range
from pandas.tseries.offsets import CDay


class PosOrderByDateReport(models.AbstractModel):
    _name = 'report.pos_order_report.report_pos_order_by_date'

    def get_date_in_utc(self, date):
        '''
        @date: it must be a string in DEFAULT_SERVER_DATETIME_FORMAT
        '''
        tz = self.env.context['tz']
        local_tz = pytz.timezone(tz)
        datetime_with_tz = local_tz.localize(date, is_dst=None)
        datetime_in_utc = datetime_with_tz.astimezone(pytz.utc)
        return datetime_in_utc.strftime(DT)

    def get_pos_orders_by_date(self, data):
        pos_order_obj = self.env['pos.order']
        rng = date_range(
            datetime.strptime(data['form']['date_start'], DF),
            datetime.strptime(data['form']['date_end'], DF),
            freq=CDay(weekmask='Mon Tue Wed Thu Fri Sat'))
        pos_order_ids = []
        for date in rng:
            date_start = date + timedelta(hours=10)
            date_start_utc = self.get_date_in_utc(date_start)
            date_end = date + timedelta(hours=18)
            date_end_utc = self.get_date_in_utc(date_end)
            pos_order = pos_order_obj.search([
                ('date_order', '>=', date_start_utc),
                ('date_order', '<=', date_end_utc),
                ('session_id.config_id', '=', data['form']['pos_config_id'][0])
                ])
            pos_order_ids.append(pos_order)
        return pos_order_ids

    def get_totals(self, data, type):
        pos_order_ids = self.get_pos_orders_by_date(data)
        result = []
        for pos_orders_by_day in pos_order_ids:
            total = 0
            for pos_order in pos_orders_by_day:
                if type == 'tax':
                    total += pos_order.amount_tax
                elif type == 'total':
                    total += pos_order.amount_total
                elif type == 'cash' or 'bank':
                    for statement in pos_order.statement_ids:
                        if statement.journal_id.type == type:
                            total += statement.amount
            result.append(total)
        return result

    def pos_order_line(self, data):
        result = []
        cash = self.get_totals(data, 'cash')
        bank = self.get_totals(data, 'bank')
        tax = self.get_totals(data, 'tax')
        total = self.get_totals(data, 'total')
        for x in range(len(cash)):
            result.append({
                'cash': cash[x],
                'bank': bank[x],
                'tax': tax[x],
                'total': total[x],
                })
        return result

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'pos_order_report.report_pos_order_by_date')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'data': data,
            'pos_order_line': self.pos_order_line,
        }
        return report_obj.render(
            'pos_order_report.report_pos_order_by_date', docargs)
