# coding: utf-8` or `# -*- coding: utf-8 -*-
from openerp import api, models
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT as DT
from datetime import datetime
import pytz
from pandas import bdate_range
from pandas.tseries.offsets import CDay


class PosOrderByDateReport(models.AbstractModel):
    _name = 'report.pos_order_report.report_pos_order_by_date'

    def get_date_in_utc(self, date):
        '''
        @date: it must be a string in DEFAULT_SERVER_DATETIME_FORMAT
        '''
        tz = self.env.context['tz']
        local_tz = pytz.timezone(tz)
        datetime_without_tz = datetime.strptime(date, DT)
        datetime_with_tz = local_tz.localize(datetime_without_tz, is_dst=None)
        datetime_in_utc = datetime_with_tz.astimezone(pytz.utc)
        return datetime_in_utc.strftime(DT)

    def get_date_range(self, date_start, date_end):
        rng = bdate_range(
            date_start,
            date_end,
            freq=CDay(weekmask='Mon Tue Wed Thu Fri Sat'))
        return rng

    def get_pos_orders_by_date(self, data):
        pos_order_obj = self.env['pos.order']
        date_start = self.get_date_in_utc(
            data['form']['date_start'] + ' 10:00:00')
        date_end = self.get_date_in_utc(
            data['form']['date_end'] + ' 18:00:00')
        pos_order_ids = pos_order_obj.search([
            ('date_order', '>=', date_start),
            ('date_order', '<=', date_end)
            ])
        return pos_order_ids

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
            'pos_order_ids': self.get_pos_orders_by_date,
        }
        return report_obj.render(
            'pos_order_report.report_pos_order_by_date', docargs)
