# -*- coding: utf-8 -*-
# Copyright 2017, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class report_account_followup_report(models.AbstractModel):
    _inherit = "account.followup.report"

    @api.model
    def get_lines(self, context_id, line_id=None, public=False):
        res = super(report_account_followup_report, self).get_lines(
            context_id, line_id, public)
        for report_part in res:
            if report_part['type'] in ['payment', 'unreconciled_aml']:
                currency_id = self.env['account.invoice'].browse(
                    report_part['action'][1]).currency_id
                report_part['columns'].insert(5, currency_id.name)
            elif report_part['type'] == 'total':
                report_part['columns'].insert(3, '')
        return res
