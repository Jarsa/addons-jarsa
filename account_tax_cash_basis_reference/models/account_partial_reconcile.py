# -*- coding: utf-8 -*-
# Copyright 2017, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, models
from openerp.exceptions import UserError


class AccountPartialReconcileCashBasis(models.Model):
    _inherit = 'account.partial.reconcile'

    def _get_tax_cash_basis_lines(self, value_before_reconciliation):
        lines, move_date = super(
            AccountPartialReconcileCashBasis, self)._get_tax_cash_basis_lines(
            value_before_reconciliation)
        for rec in self:
            ref = '/'
            partner_id = False
            if rec.debit_move_id.move_id.journal_id.type == 'sale':
                ref = rec.debit_move_id.move_id.name
                partner_id = rec.debit_move_id.move_id.partner_id
            else:
                ref = (rec.credit_move_id.move_id.ref or
                       rec.credit_move_id.move_id.name)
                partner_id = rec.credit_move_id.move_id.partner_id

        tax_accounts = []
        taxes = self.env['account.tax'].search(
            [('use_cash_basis', '=', True)])
        lines_to_unlink = []
        for tax in taxes:
            tax_accounts.append(tax.cash_basis_account)
            tax_accounts.append(tax.account_id)
            tax_accounts.append(tax.refund_account_id)
        for index in range(len(lines)):
            vals = lines[index][2]
            line_account_id = self.env['account.account'].browse(
                vals['account_id'])
            # We check if the account is not a tax account
            if line_account_id not in list(set(tax_accounts)):
                lines_to_unlink.append(lines[index])
            else:
                vals['partner_id'] = partner_id.id if partner_id else False
                vals['name'] = ref
                lines[index] = (0, 0, vals)

        # We remove the trash moves because we only need the tax moves
        for index in range(len(lines_to_unlink)):
            lines.remove(lines_to_unlink[index])
        return lines, move_date

    def create_tax_cash_basis_entry(self, value_before_reconciliation):
        line_to_create, move_date = self._get_tax_cash_basis_lines(
            value_before_reconciliation)
        tax_move = False
        ref = False
        if len(line_to_create) > 0:
            if not self.company_id.tax_cash_basis_journal_id:
                raise UserError(
                    _('There is no tax cash basis journal defined '
                        'for this company: "%s" \n'
                        'Configure it in Accounting/Configuration/Settings')
                    % (self.company_id.name))
            if self.debit_move_id.move_id.journal_id.type == 'sale':
                tax_move = self.debit_move_id.move_id
                ref = self.credit_move_id.move_id.name
            else:
                tax_move = self.credit_move_id.move_id
                ref = self.debit_move_id.move_id.name
            move_vals = {
                'journal_id': self.company_id.tax_cash_basis_journal_id.id,
                'line_ids': line_to_create,
                'tax_cash_basis_rec_id': self.id,
                'partner_id': self.credit_move_id.move_id.partner_id.id,
                'ref': ref,
            }

            if move_date > self.company_id.period_lock_date:
                move_vals['date'] = move_date
            move = self.env['account.move'].with_context(
                dont_create_taxes=True).create(move_vals)
            # post move
            move.post()
            # Assign the tax move to the invoice journal entry
            move.write({'move_id': tax_move.id})
            return move
