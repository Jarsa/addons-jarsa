# -*- coding: utf-8 -*-
# Copyright 2017, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, models


class AccountPartialReconcileCashBasis(models.Model):
    _inherit = 'account.partial.reconcile'

    @api.model
    def create(self, vals):
        res = super(AccountPartialReconcileCashBasis, self).create(vals)
        move_tax = self.env['account.move'].search(
            [('tax_cash_basis_rec_id', '=', res.id)])
        if move_tax:
            # Get the tax payment lines
            tax_payment_lines = move_tax.line_ids.filtered(
                lambda x: x.tax_line_id)
            move_lines = []
            # Get the exchange difference move
            exchange_move_id = self.env['account.move'].search(
                [('rate_diff_partial_rec_id', '=', res.id)])
            if exchange_move_id:
                # Get the axchange difference and the exchange difference
                # account
                exchange_difference = exchange_move_id.amount
                exchange_account_id = exchange_move_id.dummy_account_id
                balance = 0.0
                for tax_line in tax_payment_lines:
                    # Get the tax rate and the base rate for the compute
                    tax_rate = tax_line.tax_line_id.amount / 100
                    if tax_rate < 0.0:
                        base = tax_line.tax_line_id.amount / 100 - 1.0
                    else:
                        base = tax_line.tax_line_id.amount / 100 + 1.0
                    # Compute the tax difference
                    tax_difference = (exchange_difference / base) * tax_rate
                    # Edit the original tax payment line with the real amount
                    move_lines.append(
                        (1, tax_line.id, {
                            'debit': (
                                tax_line.debit - tax_difference if
                                tax_line.debit > 0.0 else 0.0),
                            'credit': (
                                tax_line.credit - tax_difference if
                                tax_line.credit > 0.0 else 0.0),
                        }))
                    if tax_rate < 0.0:
                        balance -= tax_difference
                    else:
                        balance += tax_difference
                # # Create a counterpart with the corresponding currency
                # # exchange account
                move_lines.append(
                    (0, 0, {
                        'account_id': exchange_account_id.id,
                        'debit': (
                            balance if
                            exchange_move_id.journal_id.
                            default_credit_account_id == exchange_account_id
                            else 0.0),
                        'credit': (
                            balance if
                            exchange_move_id.journal_id.
                            default_debit_account_id == exchange_account_id
                            else 0.0),
                        'journal_id': tax_payment_lines[0].journal_id.id,
                        'partner_id': tax_payment_lines[0].partner_id.id,
                        'name': _('Exchange Difference'),
                    }))
                move_tax.button_cancel()
                move_tax.write({
                    'line_ids': [x for x in move_lines],
                })
                move_tax.post()

                # We get the invoice number to put it in the exchange
                # difference journal entry
                reference = (
                    res.debit_move_id.move_id.name if
                    res.debit_move_id.move_id.journal_id.type == 'sale' else
                    res.credit_move_id.name)
                exchange_move_id.button_cancel()
                exchange_move_id.write({
                    'ref': reference,
                    })
        return res
