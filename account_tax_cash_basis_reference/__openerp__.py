# -*- coding: utf-8 -*-
# Copyright 2017, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Accounting - Tax Cash Basis Move Assignation",
    "version": "9.0.0.1.0",
    "category": "Accounting",
    "author": "Jarsa Sistemas",
    "website": "https://www.jarsa.com.mx",
    "depends": ["account_tax_exigible"],
    "summary": "This module assign the tax moves to the invoice moves",
    "license": "AGPL-3",
    "data": [
        'views/account_move_view.xml',
    ],
    "application": True,
    "installable": True,
}
