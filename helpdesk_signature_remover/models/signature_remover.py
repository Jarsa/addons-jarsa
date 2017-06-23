# -*- coding: utf-8 -*-
# Copyright 2017, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import fields, models


class SignatureRemover(models.Model):
    _name = 'signature.remover'

    signature = fields.Text(
        string='Signature',
    )
    name = fields.Char(
        string='Name',
    )
