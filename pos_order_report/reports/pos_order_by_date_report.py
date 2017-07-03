# coding: utf-8` or `# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timedelta

import pytz
from openerp import api, models
from openerp.tools.misc import DEFAULT_SERVER_DATE_FORMAT as DF
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT as DT

_logger = logging.getLogger(__name__)
try:
    from pandas import date_range
    from pandas.tseries.offsets import CDay
except (ImportError, IOError) as err:
    _logger.debug(err)


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

    def get_totals(self, data):
        pos_order_obj = self.env['pos.order']
        rng = date_range(
            datetime.strptime(data['form']['date_start'], DF),
            datetime.strptime(data['form']['date_end'], DF),
            freq=CDay(weekmask='Mon Tue Wed Thu Fri Sat'))
        result = []
        totals = {}
        total_total = total_bank = total_cash = total_tax = 0
        for date in rng:
            total = bank = cash = tax = 0
            date_start = date + timedelta(hours=10)
            date_start_utc = self.get_date_in_utc(date_start)
            date_end = date + timedelta(hours=18)
            date_end_utc = self.get_date_in_utc(date_end)
            pos_order = pos_order_obj.search([
                ('date_order', '>=', date_start_utc),
                ('date_order', '<=', date_end_utc),
                ('session_id.config_id', '=', data['form']['pos_config_id'][0])
                ])
            for order in pos_order:
                tax += order.amount_tax
                total_tax += order.amount_tax
                total += order.amount_total
                total_total += order.amount_total
                for statement in order.statement_ids:
                    if statement.journal_id.type == 'cash':
                        cash += statement.amount
                        total_cash += statement.amount
                    elif statement.journal_id.type == 'bank':
                        bank += statement.amount
                        total_bank += statement.amount
            result.append({
                'date': date.strftime(DF),
                'cash': cash,
                'bank': bank,
                'subtotal': total - tax,
                'tax': tax,
                'total': total,
                })
        totals['total_total'] = total_total,
        totals['total_bank'] = total_bank,
        totals['total_cash'] = total_cash,
        totals['total_tax'] = total_tax,
        totals['total_subtotal'] = total_total - total_tax,
        return {
            'result': result,
            'totals': totals,
            }

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
            'get_totals': self.get_totals,
        }
        return report_obj.render(
            'pos_order_report.report_pos_order_by_date', docargs)
