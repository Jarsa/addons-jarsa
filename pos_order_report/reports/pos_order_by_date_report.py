# coding: utf-8` or `# -*- coding: utf-8 -*-
from openerp import api, models
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT as DT
from openerp.tools.misc import DEFAULT_SERVER_DATE_FORMAT as DF
from datetime import datetime, timedelta
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
        datetime_with_tz = local_tz.localize(date, is_dst=None)
        datetime_in_utc = datetime_with_tz.astimezone(pytz.utc)
        return datetime_in_utc.strftime(DT)

    def get_pos_orders_by_date(self, data):
        pos_order_obj = self.env['pos.order']
        rng = bdate_range(
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
            [pos_order_ids.append(x.id) for x in pos_order]
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
