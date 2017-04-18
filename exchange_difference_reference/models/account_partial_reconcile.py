# -*- coding: utf-8 -*-
# Copyright 2017, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models


class AccountPartialReconcileCashBasis(models.Model):
    _inherit = 'account.partial.reconcile'

    def create_exchange_rate_entry(self, aml_to_fix, amount_diff,
                                   diff_in_currency, currency, move_date):
        line_to_reconcile, partial_rec = super(
            AccountPartialReconcileCashBasis, self).create_exchange_rate_entry(
            aml_to_fix, amount_diff, diff_in_currency, currency, move_date)
        reconcile_move_line = self.env['account.move.line'].browse(
            line_to_reconcile)
        partial_reconcile = self.browse(partial_rec)
        # We need get the customer / supplier invoice of the main partial
        # reconcile, so, we check the type of the journal to know the
        # invoice type
        reference = (
            partial_reconcile.debit_move_id.move_id.rate_diff_partial_rec_id.
            debit_move_id.move_id.name if
            partial_reconcile.debit_move_id.move_id.rate_diff_partial_rec_id.
            debit_move_id.move_id.journal_id.type == 'sale' else
            partial_reconcile.credit_move_id.move_id.rate_diff_partial_rec_id.
            debit_move_id.move_id.name)
        reconcile_move_line.move_id.write({
            'ref': reference
            })
        return line_to_reconcile, partial_rec
