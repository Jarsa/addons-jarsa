# -*- coding: utf-8 -*-
# Copyright 2017, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    fix_number = fields.Char(string="Number",)

    @api.multi
    def invoice_validate(self):
        res = super(AccountInvoice, self).invoice_validate()
        self.fix_number = self.move_id.name
        return res

    @api.multi
    def name_get(self):
        result = []
        for inv in self:
            result.append((inv.id, "%s" % (inv.fix_number)))
        return result
