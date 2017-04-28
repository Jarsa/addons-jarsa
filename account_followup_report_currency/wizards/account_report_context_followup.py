# -*- coding: utf-8 -*-
# Copyright 2017, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, models


class account_report_context_followup(models.TransientModel):
    _inherit = "account.report.context.followup"

    def get_columns_names(self):
        res = super(account_report_context_followup, self).get_columns_names()
        if not self.env.context.get('public'):
            res.insert(5, _(' Currency '))
        return res

    @api.multi
    def get_columns_types(self):
        res = super(account_report_context_followup, self).get_columns_types()
        if not self.env.context.get('public'):
            res.insert(5, 'text')
        return res
