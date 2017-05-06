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
            tax_payment_lines = move_tax.line_ids.filtered(lambda x: x.tax_line_id)
            move_lines = []
            # Find the invoice move.
            if res.debit_move_id.journal_id.type in ['sale', 'purchase']:
                invoice_move = res.debit_move_id.move_id
            else:
                invoice_move = res.credit_move_id.move_id
            # Get the exchange difference move
            exchange_move_id = self.env['account.move'].search(
                [('rate_diff_partial_rec_id', '=', res.id)])
            if exchange_move_id:
                # Get the exchange difference account
                exchange_account_id = exchange_move_id.dummy_account_id
                balance = 0.0
                for tax_line in tax_payment_lines:
                    # Find the move line of the tax from the invoice
                    invoice_tax_line = self.env['account.move.line'].search([
                        ('move_id', '=', invoice_move.id),
                        ('debit', '=', tax_line.debit),
                        ('credit', '=', tax_line.credit),
                        ('tax_line_id', '=', tax_line.tax_line_id.id)])[0]
                    # Get info needed to compute currency rate.
                    amount_currency = invoice_tax_line.amount_currency
                    currency = invoice_tax_line.currency_id
                    company_currency = self.env.user.company_id.currency_id
                    currency = currency.with_context(date=move_tax.date)
                    # Compute the new tax amount.
                    tax_amount = abs(currency.compute(
                        amount_currency, company_currency))
                    # Edit the original tax payment line with the real amount
                    move_lines.append(
                        (1, tax_line.id, {
                            'debit': (
                                tax_amount if
                                tax_line.debit > 0.0 else 0.0),
                            'credit': (
                                tax_amount if
                                tax_line.credit > 0.0 else 0.0),
                        }))
                    # Compute the tax difference
                    if tax_line.debit > 0.0:
                        tax_difference = tax_line.debit - tax_amount
                        balance += tax_difference
                    else:
                        tax_difference = tax_line.credit - tax_amount
                        balance -= tax_difference
                # Create a counterpart with the corresponding currency
                # exchange account
                move_lines.append(
                    (0, 0, {
                        'account_id': exchange_account_id.id,
                        'debit': (
                            abs(balance) if
                            exchange_move_id.journal_id.
                            default_credit_account_id == exchange_account_id
                            else 0.0),
                        'credit': (
                            abs(balance) if
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
